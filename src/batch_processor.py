import json
import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import urllib.request
import urllib.parse
import random
import pandas as pd
import os  # 添加在文件开头的导入部分
from PIL import Image

def check_dependencies():
    try:
        import pandas as pd
        import websocket
    except ImportError as e:
        print(f"错误：缺少必要的依赖包。请运行以下命令安装：")
        print("pip install pandas websocket-client")
        exit(1)

# 在主程序开始前检查依赖
check_dependencies()

# 定义一个函数来显示GIF图片
def show_gif(fname):
    # 在命令行环境中，只需打印文件保存的位置
    print(f"图片已保存到: {fname}")
    return None
# 定义一个函数向服务器队列发送提示信息
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())
# 定义一个函数来获取图片
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()
# 定义一个函数来获取历史记录
def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())
# 定义一个函数来获取图片，这涉及到监听WebSocket消息
def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    print('prompt')
    print(prompt)
    print('prompt_id:{}'.format(prompt_id))
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    print('执行完成')
                    break  # 执行完成
        else:
            continue  # 预览为二进制数据
    history = get_history(prompt_id)[prompt_id]
    print(history)
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            # 图片分支
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output
            # 视频分支
            if 'videos' in node_output:
                videos_output = []
                for video in node_output['videos']:
                    video_data = get_image(video['filename'], video['subfolder'], video['type'])
                    videos_output.append(video_data)
                output_images[node_id] = videos_output
    print('获取图片完成')
    print(output_images)
    return output_images

# 解析工作流并获取图片
def parse_workflow(ws, image_path, prompt_text, workflow_file):
    with open(workflow_file, 'r') as f:
        prompt = json.load(f)

    # Find the LoadImage node and update the image path
    for node_id, node_data in prompt.items():
        node_class = node_data['class_type']
        if node_class == 'LoadImage':
            # Update the image path for the LoadImage node to the full path
            node_data['inputs']['image'] = image_path # Use the full path
            break # Assuming only one LoadImage node needs updating

    # Find the CLIPTextEncode node and update the prompt text
    for node_id, node_data in prompt.items():
        node_class = node_data['class_type']
        if node_class == 'CLIPTextEncode':
            # Update the prompt text for the CLIPTextEncode node
            # Ensure the correct input key is used (e.g., 'text' or 'Text')
            # Based on previous successful edit, 'Text' is the correct key
            if 'Text' in node_data['inputs']:
                node_data['inputs']['Text'] = prompt_text
            elif 'text' in node_data['inputs']:
                node_data['inputs']['text'] = prompt_text
            break # Assuming only one CLIPTextEncode node needs updating

    return get_images(ws, prompt)

# 生成图像并显示
def generate_clip(image_path, prompt_text, workflow_file, idx):
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = parse_workflow(ws, image_path, prompt_text, workflow_file)
    for node_id in images:
        for image_data in images[node_id]:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_filename = "{}_{}_{}.png".format(idx, os.path.basename(image_path).split('.')[0], timestamp)
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, "wb") as binary_file:
                binary_file.write(image_data)
            print("{} DONE!!!".format(output_path))

if __name__ == "__main__":
    # 从 config.json 读取配置
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    comfyui_server_address = config.get('comfyui_server_address', '127.0.0.1:8188')
    input_path = config.get('input_path', '')
    output_dir = config.get('output_dir', 'output')
    workflow_file = config.get('workflow_path', 'workflows\\默认去除背景20250529.json')
    limit = config.get('limit', 0)

    server_address = comfyui_server_address
    client_id = str(uuid.uuid4())

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")

    image_files = []
    if os.path.isdir(input_path):
        for f in os.listdir(input_path):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_files.append(os.path.join(input_path, f))
    else:
        print(f"错误: 输入路径 '{input_path}' 不是一个有效的目录。")
        exit(1)

    if limit > 0:
        image_files = image_files[:limit]

    # 假设所有图片使用相同的 prompt
    # 您可以根据需要修改此部分，例如从 CSV 或其他来源为每张图片读取不同的 prompt
    # 这里我们使用一个默认的 prompt，或者您可以从 config.json 中读取
    default_prompt = "Toner Cartridge or Ink Cartridge" # 示例 prompt

    for idx, image_file in enumerate(image_files):
        print(f"处理图片: {image_file}")
        generate_clip(image_file, default_prompt, workflow_file, idx + 1)
import websocket
import uuid
import json
import urllib.request
import urllib.parse
import random
import time

# 客户端ID，用于标识WebSocket连接
CLIENT_ID = str(uuid.uuid4())
# 工作流API JSON文件路径
WORKFLOW_API_JSON_PATH = "..\\workflows\\workflow_api.json"  # Adjusted path

# ComfyUI服务器地址 (将从config.json加载)
COMFYUI_SERVER_ADDRESS = None

def load_config():
    """从config.json加载配置。"""
    global COMFYUI_SERVER_ADDRESS
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
    config_path = os.path.normpath(config_path)
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            COMFYUI_SERVER_ADDRESS = config.get('comfyui_server_address', '127.0.0.1:8188') # 提供默认值
            print(f"从 {config_path} 加载配置，服务器地址: {COMFYUI_SERVER_ADDRESS}")
    except FileNotFoundError:
        print(f"错误：找不到配置文件 {config_path}。将使用默认服务器地址 '127.0.0.1:8188'。")
        COMFYUI_SERVER_ADDRESS = '127.0.0.1:8188'
    except json.JSONDecodeError:
        print(f"错误：无法解析配置文件 {config_path}。将使用默认服务器地址 '127.0.0.1:8188'。")
        COMFYUI_SERVER_ADDRESS = '127.0.0.1:8188'
    except Exception as e:
        print(f"加载配置时发生未知错误: {e}。将使用默认服务器地址 '127.0.0.1:8188'。")
        COMFYUI_SERVER_ADDRESS = '127.0.0.1:8188'

def load_workflow_api(filepath):
    """从文件加载工作流API JSON。"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到工作流文件 {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"错误：无法解析工作流文件 {filepath}")
        return None

def queue_prompt(prompt_workflow, server_address, client_id):
    """向ComfyUI提交一个prompt任务。"""
    p = {"prompt": prompt_workflow, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except urllib.error.URLError as e:
        print(f"提交prompt时出错: {e}")
        return None

def get_image(filename, subfolder, folder_type, server_address):
    """从ComfyUI服务器获取图像。"""
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    image_url = f"http://{server_address}/view?{url_values}"
    print(f"正在获取图像: {image_url}")
    try:
        with urllib.request.urlopen(image_url) as response:
            return response.read()
    except urllib.error.URLError as e:
        print(f"获取图像时出错: {e}")
        return None

def get_history(prompt_id, server_address):
    """获取特定prompt_id的历史记录。"""
    history_url = f"http://{server_address}/history/{prompt_id}"
    try:
        with urllib.request.urlopen(history_url) as response:
            return json.loads(response.read())
    except urllib.error.URLError as e:
        print(f"获取历史记录时出错: {e}")
        return None

def handle_websocket_messages(ws_url, prompt_id, server_address):
    """连接到WebSocket并处理消息。"""
    ws = websocket.WebSocket()
    try:
        ws.connect(ws_url)
        print(f"已连接到WebSocket: {ws_url}")
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'status':
                    status_data = message['data']['status']
                    print(f"状态更新: 队列剩余 {status_data.get('exec_info', {}).get('queue_remaining', 'N/A')}")
                elif message['type'] == 'execution_start':
                    if message['data']['prompt_id'] == prompt_id:
                        print(f"任务 {prompt_id} 开始执行。")
                elif message['type'] == 'executing':
                    data = message['data']
                    if data['prompt_id'] == prompt_id:
                        if data['node'] is None:
                            print(f"任务 {prompt_id} 执行完毕。")
                            # 任务完成，跳出循环以获取图像
                            break 
                        else:
                            print(f"任务 {prompt_id} 正在执行节点 {data['node']}")
                elif message['type'] == 'progress':
                    data = message['data']
                    print(f"进度: {data['value']}/{data['max']}")
                else:
                    # print(f"收到未知文本消息: {message['type']}")
                    pass # 可以忽略其他类型的消息或按需处理
            elif isinstance(out, bytes):
                # print("收到二进制预览图像数据 (已忽略)")
                pass # 忽略预览图像数据
            else:
                print(f"收到未知类型消息: {type(out)}")

    except websocket.WebSocketConnectionClosedException:
        print("WebSocket 连接已关闭。")
    except ConnectionRefusedError:
        print("WebSocket 连接被拒绝。请确保ComfyUI服务器正在运行并且WebSocket服务可用。")
    except Exception as e:
        print(f"WebSocket 错误: {e}")
    finally:
        if ws.connected:
            ws.close()
            print("WebSocket 连接已关闭。")

import os

def main(input_image_path=None, output_directory='.'):
    load_config() # 在main函数开始时加载配置
    if not COMFYUI_SERVER_ADDRESS:
        print("错误: ComfyUI服务器地址未配置。请检查config.json文件或错误日志。")
        return

    print("ComfyUI API 客户端启动")
    print(f"服务器地址: {COMFYUI_SERVER_ADDRESS}")
    print(f"客户端ID: {CLIENT_ID}")

    # 1. 加载工作流
    # 构建工作流文件的绝对路径，以确保在任何位置运行run.py时都能找到它
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_workflow_path = os.path.join(current_script_dir, WORKFLOW_API_JSON_PATH)
    # 规范化路径，处理 ".."
    absolute_workflow_path = os.path.normpath(absolute_workflow_path)
    
    prompt_workflow = load_workflow_api(absolute_workflow_path)
    if not prompt_workflow:
        return

    # 修改输入图像 (假设节点 '36' 是 LoadImage 节点)
    if input_image_path:
        if "36" in prompt_workflow and "inputs" in prompt_workflow["36"]:
            prompt_workflow["36"]["inputs"]["image"] = os.path.basename(input_image_path) # ComfyUI通常需要相对于其输入目录的文件名
            # 注意：ComfyUI的LoadImage节点通常需要图片在其input目录中，或者需要配置ComfyUI以允许从其他路径加载
            # 这里我们假设图片名是ComfyUI可以访问的，或者工作流配置了绝对路径加载（不常见）
            # 更健壮的做法是确保图片在ComfyUI的input文件夹下，或者使用API上传图片
            print(f"设置输入图像为: {os.path.basename(input_image_path)} (节点 36)")
        else:
            print("警告: 工作流中未找到节点 '36' 或其输入设置，无法设置输入图像。")
    else:
        print("未提供输入图像路径，将使用工作流中的默认图像。")
    
    # 示例：修改提示词 (假设节点 '32' 是 LLM 节点, 'user_prompt' 是其输入之一)
    # prompt_workflow["32"]["inputs"]["user_prompt"] = "A beautiful landscape painting."

    # 2. 提交任务
    print("\n正在提交任务到ComfyUI...")
    queue_response = queue_prompt(prompt_workflow, COMFYUI_SERVER_ADDRESS, CLIENT_ID)
    if not queue_response or 'prompt_id' not in queue_response:
        print("无法提交任务或获取prompt_id。")
        if queue_response and 'node_errors' in queue_response and queue_response['node_errors']:
            print("节点错误:", json.dumps(queue_response['node_errors'], indent=2))
        return
    
    prompt_id = queue_response['prompt_id']
    print(f"任务已提交，Prompt ID: {prompt_id}")
    if 'number' in queue_response:
        print(f"当前任务序号: {queue_response['number']}")

    # 3. 通过WebSocket监听进度
    ws_url = f"ws://{COMFYUI_SERVER_ADDRESS}/ws?clientId={CLIENT_ID}"
    print(f"\n正在连接WebSocket: {ws_url}")
    handle_websocket_messages(ws_url, prompt_id, COMFYUI_SERVER_ADDRESS)

    # 4. 获取历史记录和输出图像
    print(f"\n任务 {prompt_id} 完成，正在获取结果...")
    time.sleep(1) # 等待一小段时间，确保历史记录已更新
    history = get_history(prompt_id, COMFYUI_SERVER_ADDRESS)

    if not history or prompt_id not in history:
        print(f"无法获取任务 {prompt_id} 的历史记录。")
        return

    prompt_history = history[prompt_id]
    if 'outputs' not in prompt_history:
        print(f"历史记录中未找到输出: {prompt_id}")
        return

    outputs = prompt_history['outputs']
    image_count = 0
    for node_id in outputs:
        node_output = outputs[node_id]
        if 'images' in node_output:
            for image_data in node_output['images']:
                if image_data['type'] == 'output' or image_data['type'] == 'temp': # 根据需要处理temp或output类型
                    image_bytes = get_image(image_data['filename'], 
                                            image_data.get('subfolder', ''), 
                                            image_data['type'], 
                                            COMFYUI_SERVER_ADDRESS)
                    if image_bytes:
                        image_count += 1
                        # 获取源文件名 (假设节点 '36' 是 LoadImage 节点)
                        source_image_name = "unknown_source"
                        if prompt_workflow and "36" in prompt_workflow and "inputs" in prompt_workflow["36"] and "image" in prompt_workflow["36"]["inputs"]:
                            source_image_name = prompt_workflow["36"]["inputs"]["image"]
                            # 移除扩展名，保留基本名
                            source_image_basename = source_image_name.rsplit('.', 1)[0] if '.' in source_image_name else source_image_name
                        else:
                            source_image_basename = "unknown_source"
                        
                        # 使用源文件名、prompt_id 和 ComfyUI 生成的文件名（不含扩展名）构建新文件名
                        comfyui_generated_basename = image_data['filename'].rsplit('.', 1)[0] if '.' in image_data['filename'] else image_data['filename']
                        file_extension = image_data['filename'].rsplit('.', 1)[1] if '.' in image_data['filename'] else 'png' # 默认png

                        output_filename = f"output_{source_image_basename}_{comfyui_generated_basename}_{prompt_id}_{image_count}.{file_extension}"
                        output_filepath = os.path.join(output_directory, output_filename)
                        try:
                            with open(output_filepath, 'wb') as f:
                                f.write(image_bytes)
                            print(f"图像已保存: {output_filepath}")
                        except IOError as e:
                            print(f"保存图像时出错 {output_filepath}: {e}")
                    else:
                        print(f"无法获取图像: {image_data['filename']}")
    
    if image_count == 0:
        print("未找到或保存任何输出图像。")
        print("历史输出详情:", json.dumps(outputs, indent=2))

    print("\nComfyUI API 客户端执行完毕。")

if __name__ == "__main__":
    main()
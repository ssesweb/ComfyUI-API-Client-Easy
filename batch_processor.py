import os
import json
import uuid
import requests
from websocket import create_connection
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class ComfyUIBatchProcessor:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.workflow = self.load_workflow()
        self.input_files = self.get_input_files()
        self.identified_nodes = self.identify_workflow_nodes()
        
    def load_config(self, config_path):
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config["input_path"] = Path(config["input_path"])
        config["output_dir"] = Path(config["output_dir"])
        config["workflow_path"] = Path(config["workflow_path"])
        return config

    def load_workflow(self):
        """加载工作流模板"""
        with open(self.config["workflow_path"], 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_input_files(self):
        """获取输入目录中的图像文件"""
        input_path = self.config["input_path"]
        limit = self.config["limit"]
        
        image_files = [
            f for f in input_path.iterdir() 
            if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']
        ]
        
        return image_files[:limit] if limit > 0 else image_files

    def identify_workflow_nodes(self):
        """识别工作流中的关键节点"""
        nodes = {
            "load_image": None,
            "save_image": None
        }
        
        for node_id, node_data in self.workflow.items():
            if node_data.get("class_type") == "LoadImage":
                nodes["load_image"] = node_id
            elif node_data.get("class_type") == "SaveImage":
                nodes["save_image"] = node_id
                
        return nodes

    def modify_workflow(self, original_image_path, uploaded_filename):
        """修改工作流以处理当前图像"""
        workflow_copy = json.loads(json.dumps(self.workflow))  # Deep copy
        
        # 更新输入图像路径
        if self.identified_nodes["load_image"]:
            node_id = self.identified_nodes["load_image"]
            # ComfyUI的LoadImage节点需要的是文件名，而不是完整路径
            workflow_copy[node_id]["inputs"]["image"] = uploaded_filename
        
        # 更新输出文件名（可选）
        if self.identified_nodes["save_image"]:
            node_id = self.identified_nodes["save_image"]
            filename_prefix = f"{original_image_path.stem}_processed"
            workflow_copy[node_id]["inputs"]["filename_prefix"] = filename_prefix
        
        return workflow_copy

    def submit_prompt(self, workflow_data):
        """提交任务到ComfyUI"""
        client_id = str(uuid.uuid4())
        url = f"http://{self.config['comfyui_server_address']}/prompt"
        
        payload = {
            "client_id": client_id,
            "prompt": workflow_data
        }
        print(f"\nWorkflow Data: {json.dumps(workflow_data, indent=2)}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error submitting prompt: {e}")
            if e.response is not None:
                print(f"Response content: {e.response.text}")
            raise
        
        return response.json()["prompt_id"], client_id

    def monitor_progress(self, client_id):
        """通过WebSocket监控任务进度"""
        ws_url = f"ws://{self.config['comfyui_server_address']}/ws?clientId={client_id}"
        ws = create_connection(ws_url)
        
        try:
            while True:
                message = ws.recv()
                if isinstance(message, str):
                    data = json.loads(message)
                    
                    # 检测任务完成
                    if data.get("type") == "executing" and data.get("data", {}).get("node") is None:
                        return True
        finally:
            ws.close()

    def download_result(self, prompt_id, output_path):
        """下载处理结果"""
        # 获取历史记录
        history_url = f"http://{self.config['comfyui_server_address']}/history/{prompt_id}"
        history = requests.get(history_url).json().get(prompt_id, {})
        
        # 定位输出图像
        output_node_id = self.identified_nodes["save_image"]
        if not output_node_id or output_node_id not in history.get("outputs", {}):
            raise ValueError("Output image node not found in results")
        
        image_info = history["outputs"][output_node_id]["images"][0]
        
        # 下载图像
        params = {
            "filename": image_info["filename"],
            "type": image_info["type"],
            "subfolder": image_info.get("subfolder", "")
        }
        
        download_url = f"http://{self.config['comfyui_server_address']}/view"
        response = requests.get(download_url, params=params, stream=True)
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return output_path

    def upload_image(self, image_path, image_type="input", subfolder=""):
        """上传图片到ComfyUI服务器"""
        url = f"http://{self.config['comfyui_server_address']}/upload/image"
        files = {'image': (image_path.name, open(image_path, 'rb'), 'image/png')}
        data = {'type': image_type, 'subfolder': subfolder}
        
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()

    def process_image(self, image_path):
        """处理单个图像"""
        try:
            # 准备处理
            # 先上传图片到ComfyUI服务器
            print(f"Uploading image: {image_path.name}")
            upload_result = self.upload_image(image_path)
            uploaded_filename = upload_result['name']
            
            # 修改工作流以使用上传后的图片文件名
            workflow_data = self.modify_workflow(image_path, uploaded_filename)
            output_path = self.config["output_dir"] / f"{image_path.stem}_processed.png"
            
            # 提交任务
            prompt_id, client_id = self.submit_prompt(workflow_data)
            
            # 监控进度
            self.monitor_progress(client_id)
            
            # 获取结果
            self.download_result(prompt_id, output_path)
            
            return True, output_path
        
        except Exception as e:
            return False, str(e)

    def run_batch_processing(self, max_workers=3):
        """批量处理所有图像"""
        self.config["output_dir"].mkdir(parents=True, exist_ok=True)
        success_count = 0
        error_log = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.process_image, img): img.name
                for img in self.input_files
            }
            
            for future in futures:
                img_name = futures[future]
                try:
                    success, result = future.result()
                    if success:
                        success_count += 1
                    else:
                        error_log.append(f"{img_name}: {result}")
                except Exception as e:
                    error_log.append(f"{img_name}: {str(e)}")
        
        # 生成报告
        report = {
            "total": len(self.input_files),
            "success": success_count,
            "errors": error_log
        }
        
        return report

if __name__ == "__main__":
    config_path = "config.json"
    processor = ComfyUIBatchProcessor(config_path)
    report = processor.run_batch_processing()
    print("\nBatch Processing Report:")
    print(f"Total images processed: {report['total']}")
    print(f"Successfully processed: {report['success']}")
    if report['errors']:
        print("Errors occurred during processing:")
        for error in report['errors']:
            print(f"- {error}")
    else:
        print("All images processed successfully!")
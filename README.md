# ComfyUI API Client

[中文版](README.zh.md)


This project provides a Python client to interact with a ComfyUI instance for image processing tasks.

## Features

- Submit image processing jobs to ComfyUI using a predefined workflow.
- Monitor job progress via WebSocket.
- Retrieve processed images.

## Prerequisites

- Python 3.8+
- A running ComfyUI instance (e.g., at `http://127.0.0.1:8188`)

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 通过API运行工作流

1.  **配置ComfyUI服务器地址**: 
    *   在项目根目录下找到 `config.json` 文件。
    *   修改 `comfyui_server_address` 字段为您ComfyUI服务器的实际地址和端口。例如：`"comfyui_server_address": "your_server_ip:port"`。
    *   如果 `config.json` 文件不存在或无法正确解析，脚本将默认使用 `127.0.0.1:8188`。
2.  确保您的ComfyUI服务器正在运行，并且可以通过配置的地址访问。
3.  打开命令行或终端。
4.  导航到项目的根目录 (`Comfyui_Test`)。
5.  运行以下命令，替换 `<你的图片路径>` 和 `<你的输出目录>` 为实际路径：
    ```bash
    python run.py "<你的图片路径>" "<你的输出目录>"
    ```
    例如:
    ```bash
    python run.py "C:\path\to\your\image.jpg" "C:\path\to\your\output_folder"
    ```
6.  脚本将连接到ComfyUI，提交工作流，并通过WebSocket监控进度。处理完成后，输出的图像将保存在您指定的输出目录中。

## Workflow

The client uses the workflow defined in `workflows/workflow_api.json`.

## API Reference

Refer to `docs/stable_diffusion_comfyui_api_tutorial.md` for details on ComfyUI API endpoints and WebSocket communication.
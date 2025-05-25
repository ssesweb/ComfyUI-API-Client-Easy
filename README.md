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

To run the workflow via the API, you first need to configure the ComfyUI server address. This is done by editing the `config.json` file located in the project root directory.

1.  Open the `config.json` file.
2.  Modify the `comfyui_server_address` field to your ComfyUI server's address and port.
    *   **For local servers or direct IP/hostname access:** Use the format `"hostname:port"` or `"ip_address:port"` (e.g., `"127.0.0.1:8188"`, `"your-comfyui-server.com:8188"`). The script will automatically prepend `http://` for HTTP requests and `ws://` for WebSocket connections.
    *   **For remote servers behind a proxy or requiring HTTPS:** If your server URL is something like `https://your-proxy.com/comfyui-api/`, you should typically enter the core part that the script will use to construct HTTP and WebSocket URLs. For example, if the ComfyUI API is accessible at `your-proxy.com/comfyui-api/` (and websockets at `wss://your-proxy.com/comfyui-api/ws`), you might need to configure it as `"your-proxy.com/comfyui-api"`. The script currently assumes HTTP/WS, so for HTTPS/WSS, you might need to adjust the script or ensure your proxy handles the protocol upgrade. **It's crucial to ensure the address in `config.json` correctly points to the ComfyUI API endpoint without the protocol prefix (`http://` or `https://`) unless your setup specifically requires it and the script is modified to handle it.**
    *   **Example for a proxied HTTPS URL like `https://567795-proxy-8188.dsw-gateway-cn-shanghai.data.aliyun.com/`:** If this URL directly serves the ComfyUI API (including WebSocket on the same base path), you would likely set `comfyui_server_address` to `"567795-proxy-8188.dsw-gateway-cn-shanghai.data.aliyun.com"`. The script will attempt to connect via `http://` and `ws://`. If the service requires `https://` and `wss://`, the client script (`src/comfyui_client.py`) would need modification to support these protocols explicitly.

If the `config.json` file does not exist or cannot be parsed, the script will default to using `127.0.0.1:8188`.
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
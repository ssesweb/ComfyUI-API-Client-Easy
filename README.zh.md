# ComfyUI API 客户端

本项目提供了一个 Python 客户端，用于与 ComfyUI 实例进行交互，以执行图像处理任务。

## 功能

- 使用预定义的工作流向 ComfyUI 提交图像处理作业。
- 通过 WebSocket 监控作业进度。
- 检索处理后的图像。

## 先决条件

- Python 3.8+
- 一个正在运行的 ComfyUI 实例 (例如，在 `http://127.0.0.1:8188`)

## 设置

1. 克隆此仓库：
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
2. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

## 用法

### 通过API运行工作流

1.  **配置ComfyUI服务器地址**：
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
    例如：
    ```bash
    python run.py "C:\path\to\your\image.jpg" "C:\path\to\your\output_folder"
    ```
6.  脚本将连接到ComfyUI，提交工作流，并通过WebSocket监控进度。处理完成后，输出的图像将保存在您指定的输出目录中。

## 工作流

客户端使用 `workflows/workflow_api.json` 中定义的工作流。

## API 参考

有关 ComfyUI API 端点和 WebSocket 通信的详细信息，请参阅 `docs/stable_diffusion_comfyui_api_tutorial.md`。
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

要通过API运行工作流，您首先需要配置ComfyUI服务器的地址。这可以通过编辑项目根目录下的 `config.json` 文件来完成。

1.  打开 `config.json` 文件。
2.  将 `comfyui_server_address` 字段修改为您的ComfyUI服务器的地址和端口。
    *   **对于本地服务器或直接IP/主机名访问：** 使用格式 `"主机名:端口"` 或 `"IP地址:端口"` (例如, `"127.0.0.1:8188"`, `"your-comfyui-server.com:8188"`)。脚本会自动为HTTP请求添加 `http://` 前缀，为WebSocket连接添加 `ws://` 前缀。
    *   **对于位于代理之后或需要HTTPS的远程服务器：** 如果您的服务器URL类似于 `https://your-proxy.com/comfyui-api/`，您通常需要输入核心部分，脚本将使用该部分构建HTTP和WebSocket URL。例如，如果ComfyUI API可在 `your-proxy.com/comfyui-api/` 访问（WebSocket在 `wss://your-proxy.com/comfyui-api/ws`），您可能需要将其配置为 `"your-proxy.com/comfyui-api"`。脚本目前假定使用HTTP/WS，因此对于HTTPS/WSS，您可能需要调整脚本或确保您的代理处理协议升级。**关键是要确保 `config.json` 中的地址正确指向ComfyUI API端点，不带协议前缀（`http://` 或 `https://`），除非您的设置特别需要并且脚本已修改以处理它。**
    *   **例如，对于像 `https://567795-proxy-8188.dsw-gateway-cn-shanghai.data.aliyun.com/` 这样的代理HTTPS URL：** 如果此URL直接提供ComfyUI API（包括在同一基本路径上的WebSocket），您可能需要将 `comfyui_server_address` 设置为 `"567795-proxy-8188.dsw-gateway-cn-shanghai.data.aliyun.com"`。脚本将尝试通过 `http://` 和 `ws://` 连接。如果服务需要 `https://` 和 `wss://`，则客户端脚本（`src/comfyui_client.py`）将需要修改以显式支持这些协议。

如果 `config.json` 文件不存在或无法解析，脚本将默认使用 `127.0.0.1:8188`。
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
# ComfyUI-API-Client-Easy

这是一个用于与 ComfyUI API 交互的 Python 客户端，旨在简化批量图像处理工作流。

## 功能

- 从配置文件 (`config.json`) 读取 ComfyUI 服务器地址、输入/输出目录和工作流文件。
- 批量处理指定输入目录中的图像文件。
- 支持通过 `config.json` 中的 `limit` 参数限制处理的图像数量。
- 使用 WebSocket 与 ComfyUI 服务器通信，发送工作流并获取处理结果。
- 自动将处理后的图像保存到指定输出目录。

## 安装

1. 克隆此仓库：
   ```bash
   git clone https://github.com/ssesweb/ComfyUI-API-Client-Easy.git
   cd ComfyUI-API-Client-Easy
   ```

2. 安装必要的 Python 依赖：
   ```bash
   pip install -r requirements.txt
   ```
   (注意：`requirements.txt` 文件可能需要手动创建或根据 `batch_processor.py` 中的 `check_dependencies` 函数提示安装 `pandas` 和 `websocket-client`)

## 使用方法

1. **配置 `config.json` 文件**：
   - `comfyui_server_address`: 您的 ComfyUI 服务器地址 (例如: `127.0.0.1:8188`)
   - `input_path`: 包含待处理图像的输入目录路径。
   - `output_dir`: 处理后图像的输出目录路径。
   - `workflow_path`: ComfyUI 工作流 JSON 文件的路径 (例如: `workflows\\默认去除背景20250529.json`)
   - `limit`: 限制处理的图像数量。设置为 `0` 表示处理所有图像。

   示例 `config.json`:
   ```json
   {
       "comfyui_server_address": "127.0.0.1:8188",
       "input_path": "C:\\Users\\Adminstor\\Downloads\\1688pics",
       "output_dir": "C:\\Users\\Adminstor\\Downloads\\1688_Comfyui_Pics",
       "workflow_path": "workflows\\默认去除背景20250529.json",
       "limit": 0
   }
   ```

2. **运行 `batch_processor.py`**：
   ```bash
   python src/batch_processor.py
   ```

程序将读取配置，连接到 ComfyUI 服务器，并开始批量处理图像。

## 注意事项

- 确保您的 ComfyUI 服务器正在运行并可通过 `comfyui_server_address` 访问。
- 工作流文件 (`.json`) 必须是有效的 ComfyUI API 工作流。
- `LoadImage` 节点在工作流中应配置为接收完整的文件路径。
- 如果遇到 `UnicodeDecodeError`，请确保您的工作流文件以 UTF-8 编码保存。

## 贡献

欢迎贡献！如果您有任何改进建议或发现 Bug，请随时提交 Pull Request 或 Issue。
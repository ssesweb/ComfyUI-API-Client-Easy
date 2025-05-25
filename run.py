import sys
import os

# 将src目录添加到Python路径，以便可以导入comfyui_client
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'src'))

import argparse
from comfyui_client import main as comfyui_main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ComfyUI client with specified input image and output directory.")
    parser.add_argument("input_image", type=str, help="Path to the input image file.")
    parser.add_argument("output_dir", type=str, help="Directory to save the output images.")

    args = parser.parse_args()

    # 确保输出目录存在
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Created output directory: {args.output_dir}")

    print(f"Executing ComfyUI client from: {os.path.join(current_dir, 'src', 'comfyui_client.py')}")
    print(f"Input image: {args.input_image}")
    print(f"Output directory: {args.output_dir}")
    
    comfyui_main(input_image_path=args.input_image, output_directory=args.output_dir)
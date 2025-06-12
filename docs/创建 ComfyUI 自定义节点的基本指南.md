ComfyUI 是一个多功能的Stable Diffusion图像/视频生成工具，能够让开发者设计并实现自定义节点，扩展功能。如果你有特定的任务想实现并需要创建一个自定义节点，本指南会带你一步步完成 ComfyUI 自定义节点的创建过程。

开始前的准备
在开始创建自定义节点之前，确保你有必要的工具。你需要一个强大的代码编辑器，比如 Visual Studio Code，并安装 Python 和 JavaScript 的开发扩展。另外，具备 Python 和 JavaScript 的基础知识也很重要。

理解 ComfyUI 节点
ComfyUI 采用基于节点的架构，其中 UI 元素被表示为相互连接的节点。每个节点封装了特定的功能或行为，使得 UI 开发模块化且可扩展。开发者可以创建自定义节点，以满足项目需求，扩展 ComfyUI 的功能。

创建自定义节点
让我们来看看如何使用 Python 和 JavaScript 为 ComfyUI 创建自定义节点。

1. 定义节点参数
首先定义你的自定义节点的参数和属性。这些参数决定了节点在UI界面中的用途和外观。以下是一个简单的自定义节点定义案例，输入一个整数，输出另一个整数。创建并编辑一个名为 BasicTutorialTimesTwo.py 的文件：

class TimesTwo:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "input1": ("INT", {}),
            }
        }
        return inputs
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("RETURN VALUE",)
    FUNCTION = "AnyFunctionNameCanGoHere_SeeStep2"
    CATEGORY = "CivitaiTutorials/BasicNodes"
2. 实现节点逻辑
接下来，实现自定义节点的逻辑和功能。这可能涉及处理用户输入、执行计算或与外部数据源交互。这些处理是在步骤 1 中指定的函数中完成的：

def funcTimesTwo(self, input1):
    returnval = 0
    returnval = input1 * 2
    return (returnval,)
把这些结合起来，完整的类如下所示：

class TimesTwo:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "input1": ("INT", {}),
            }
        }
        return inputs
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("RETURN VALUE",)
    FUNCTION = "funcTimesTwo"
    CATEGORY = "CivitaiTutorials/BasicNodes"
    def funcTimesTwo(self, input1):
        returnval = 0
        returnval = input1 * 2
        return (returnval,)
3. 与 ComfyUI 集成
最后，将你的自定义节点与 ComfyUI 框架集成，使其在 UI 编辑器中可用。将你的节点注册到 ComfyUI 的节点注册表中，让用户可以轻松地将其添加到项目中。
编辑你的 __init__.py 文件，使其如下所示：

from .BasicTutorialTimesTwo import TimesTwo
NODE_CLASS_MAPPINGS = {
    "btTimesTwo": TimesTwo
}
NODE_DISPLAY_NAMES_MAPPINGS = {
    "btTimesTwo": "Basic Tutorial - Times Two"
}
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAMES_MAPPINGS']
此时，你可以测试节点了。加载 ComfyUI 并打开你的网页浏览器进入 ComfyUI 界面。在空白区域右键点击以添加一个节点。如果一切设置正确，你应该会看到一个新的菜单选项 CivitaiTutorials。在这个菜单下应该有一个子菜单 BasicNodes，在那里你会找到我们刚刚创建的节点。
在这里插入图片描述
在这里插入图片描述

测试和改进节点
添加节点后，你可能会发现：

需要手动输入值。
没有检查输出的方法。
为了解决这些问题：
右键点击新节点并选择“将 input1 转换为输入”。
在这里插入图片描述
将输出连接到显示文本的节点。
为了实现更高级的功能，可以考虑安装额外的节点包，比如 ComfyUI-quadMoons-nodes 和 ComfyUI-CustomScripts。这些包提供将整数转换为字符串并显示文本的节点。连接这些节点，你就能看到自定义节点的输出。

结论
如果一切顺利，你已经成功创建并集成了一个自定义节点到 ComfyUI 中。由于 ComfyUI 是用 Python 编写的，你可以通过查看其源代码来发现更多节点开发的可能性。祝你在开发过程中好运，编码愉快！

如果需要开发Comfyui自定义节点或者工作流，以及将工作流封装成软件、网站、小程序的话，可以看我的另外一篇文章：
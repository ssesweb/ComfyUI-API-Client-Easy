https://blog.csdn.net/jjs15259655776/article/details/134388940
一、为什么要使用comfyui的api?对比webui的api，它有什么好处？
1、自带队列
2、支持websocket
3、无需关心插件是否有开放api接口，只要插件在浏览器中可以正常使用，接口就一定可以使用
4、开发人员只需关心绘图流程的搭建
5、切换模型、进度查询soeasy
6、轻松实现图片生成时的渐变效果
7、支持中断绘图任务
8、无需繁琐的base64图片转换

其实我们之前一直都是用web-ui的api,最近web-ui被我们给废弃掉了，主要是因为comfyui基本上解决了webui做开发所有的弊端，首先列队的问题不用去管，它自己有列队，插件这块是最方便的，用上comfyui以后就不要去管插件是怎么调用的，只要你在工作流里面用了什么插件，保存为api之后，他直接下发后台就会自动去运行，也不用去管插件具体怎么调用。如果是webui,有些比较良心的插件，直接把接口写好，然后暴露出来， 如果没写的话，你用起来就会非常的麻烦，还得去研究它是怎么去调用的。所以 ，小伙伴们，别再执着用webui的api了,那个确实反人类，假如做开发的话问题会很多，比较烦人，就像获取任务进度，还有这个线程锁，切换模型这块都非常繁琐。我为了研究那东西 ，看代码看得头都大了 ，整整研究了一个月才把代码改好。

二、接口详解
本文主要介绍 stable diffusion API 调用，准确来说是对 stable diffusion comfyui 的 API 调用。需要apifox接口文件的可以查看：
https://gitee.com/BTYY/wailikeji-chatgpt/blob/master/comfyui-api.md

1、绘图接口：POST /prompt
注意：该接口只做绘图任务的下发，然后返回任务ID信息。并不会直接返回最终的结果图！

与webui的api不同的是，comfyui的api并没有单独区分文生图、图生图的接口，而是所有的绘图任务的下发全部都使用POST /prompt。那具体是文生图、图生图、又或者是换脸、倒推关键词等，取决于你的参数！

需要上传的参数只有两个

请求参数
名称	类型	必选	说明
client_id	string	是	任务ID,由客户端生成，用于标记任务是谁发起的
prompt	json	是	任务参数
返回参数
名称	类型	说明
prompt_id	string	任务ID
number	int	当前任务序号，可用于后续获取需要等待任务数的计算
node_errors	json	错误信息
返回示例

{
    "prompt_id": "bd2cfa2c-de87-4258-89cc-d8791bc13a61",
    "number": 501,
    "node_errors": {}
}
1
2
3
4
5
使用说明
clientId：任务ID,由客户端生成，用于标记任务是谁发起的,相当于告诉comfyui，该绘图任务是由用户A发起的，后续comfyui就会通过websocket将属于用户A的绘图信息推送给你

prompt：prompt所传的是一个json数据，它是由comfyui浏览器通过保存api生成的json数据，如下图
在这里插入图片描述

至于正反、提示词、模型、vae、图片尺寸、批次、提示词相关性、随机种子、采样器、降噪值等参数，只需替换json中对应的参数为用户上传的参数即可
在这里插入图片描述
比如用户上传的图片尺寸是768*512，那你只需将json数据中的width改为768、height改为512即可，其他的参数也是同样的道理！

2、websocket：/ws?clientId=XXXXXXXX
client_id后面的参数即为上面/prompt接口中上传给comfyui的client_id，假如没有上传client_id，那comfyui就不知道连上该websocket的用户是谁，也就无法进行信息推送！comfyui拿到client_id后，即可知道当前是哪个用户，后续就会通过websocket将属于该用户的绘图信息精准推送给他

注意：websocket只需做监听处理，无需通过websocket向comfyui发送任何消息

websocket数据解析：
主要有两种数据格式：
1、文本数据，文本数据主要通知以下几个绘图信息：
通知任务变更、当前执行的步骤、进度
2、二进制数据，即图片预览信息

（一）文本数据详解：
（1）任务变更通知：
{
    "type":"status",
    "data":{
        "status":{
            "exec_info":{
                "queue_remaining":7
            }
        }
    }
}
1
2
3
4
5
6
7
8
9
10
当你收到type为status信息时，这是comfyui在告诉你，当前任务数发生变更，queue_remaining是指当前还有多少个任务需要处理。

注意，此处的queue_remaining并不是告诉你在你的任务之前还有多少个任务需要处理！而是总的！
所以，如果你也想像我一样（见下图），当还没轮到你的绘图任务时，显示还需等待多少个任务，你就需要借助comfyui的另一个接口：GET /queue：获取详细任务队列信息，正在运行的以及挂起的。该接口会返回挂起的任务信息，其中有prompt_id信息和number信息，你可以根据这number信息获取到当前任务排在第几位。具体如何调用，这里就不进行展开！

在这里插入图片描述

（2）当前任务开始执行：
{
    "type":"execution_start",
    "data":{
        "prompt_id":"3935f7c3-ec38-4d94-843f-86fe86c6d384"
    }
}
1
2
3
4
5
6
当你收到type为execution_start信息时，这是comfyui在告诉你，你的任务id，prompt_id为“3935f7c3-ec38-4d94-843f-86fe86c6d384”的任务当前正在被执行

（3）当前任务执行的步骤信息：
{
    "type":"executing",
    "data":{
        "node":"5",
        "prompt_id":"3935f7c3-ec38-4d94-843f-86fe86c6d384"
    }
}
1
2
3
4
5
6
7
当你收到type为executing信息时，这是comfyui在告诉你，你的任务id，prompt_id为“3935f7c3-ec38-4d94-843f-86fe86c6d384”的任务当前正在执行节点5的步骤，此处你可以解析到前端，显示当前执行的步骤名称，如下图所示
在这里插入图片描述

（4）当前进度信息：
{
    "type":"progress",
    "data":{
        "value":1,
        "max":10
    }
}
1
2
3
4
5
6
7
当你收到type为progress信息时，这是comfyui在告诉你，当前步骤执行的进度，value是当前的步数，max是总的步数，如下图所示
在这里插入图片描述

（5）绘图结束：
{
    "type":"executing",
    "data":{
        "node":null,
        "prompt_id":"37099310-a790-44f4-8d13-4f4d5f69c891"
    }
}
1
2
3
4
5
6
7
绘图结束时，type类型仍然是executing，和前面的（3）是一样的，区别主要在于node为null,也就是当type=executing,且node=null的时候，说明流程已经跑完，此时需要通过接口GET /history/{prompt_id}获取输出的图片信息。底下是通过history获取到的图片信息：

{
    "37099310-a790-44f4-8d13-4f4d5f69c891": {
    	略。。。。。。。。。。
        "outputs": {
            "18": {
                "images": [
                    {
                        "filename": "ComfyUI_temp_slqio_00001_.png",
                        "subfolder": "",
                        "type": "temp"
                    },
                    {
                        "filename": "ComfyUI_temp_slqio_00002_.png",
                        "subfolder": "",
                        "type": "temp"
                    },
                    {
                        "filename": "ComfyUI_temp_slqio_00003_.png",
                        "subfolder": "",
                        "type": "temp"
                    },
                    {
                        "filename": "ComfyUI_temp_slqio_00004_.png",
                        "subfolder": "",
                        "type": "temp"
                    }
                ]
            },
            "22": {
                "images": [
                    {
                        "filename": "ComfyUI_temp_rfvdr_00001_.png",
                        "subfolder": "",
                        "type": "temp"
                    },
                    {
                        "filename": "ComfyUI_temp_rfvdr_00002_.png",
                        "subfolder": "",
                        "type": "temp"
                    },
                    {
                        "filename": "ComfyUI_temp_rfvdr_00003_.png",
                        "subfolder": "",
                        "type": "temp"
                    },
                    {
                        "filename": "ComfyUI_temp_rfvdr_00004_.png",
                        "subfolder": "",
                        "type": "temp"
                    }
                ]
            },
            "24": {
                "images": [
                    {
                        "filename": "ComfyUI_00702_.png",
                        "subfolder": "",
                        "type": "output"
                    },
                    {
                        "filename": "ComfyUI_00703_.png",
                        "subfolder": "",
                        "type": "output"
                    },
                    {
                        "filename": "ComfyUI_00704_.png",
                        "subfolder": "",
                        "type": "output"
                    },
                    {
                        "filename": "ComfyUI_00705_.png",
                        "subfolder": "",
                        "type": "output"
                    }
                ]
            }
        }
    }
}

outputs中的内容就是最终生成的图片信息，我们通过将图片信息进行拼接，即可获取到图片的url访问地址，
例如：ComfyUI_00702_.png这张图片，其拼接后的访问地址就是：
http://127.0.0.1:8188/view?filename=ComfyUI_00702_.png&type=output

该地址实际是使用了comfyui的view接口

3、图片的在线预览接口：GET /view
图片的在线预览接口（上传图像，生图图像，蒙蔽图像，均通过该接口预览）

请求参数
名称	位置	类型	必选	说明
filename	query	string	是	图片名称
type	query	string	否	图片存放位置的文件夹（input为长传图片，output为生成的图片）
subfolder	query	string	否	子文件夹(没有可不填)
preview	query	string	否	预览
channel	query	string	否	无
在前面的websocket中，我们通过history获取最终的图片信息，我们将图片信息进行拼接，即可获取到图片的url访问地址，就是通过该接口获取到图片

（二）二进制数据详解：
二进制数据就是在绘图过程中，如果在采样器中有开启图片预览，则comfyui会以二进制数据的方式推送给你，如果没有开启，则没有，如下：
请添加图片描述

总结
至此，stable diffusion comfyui的api的整个调用逻辑已经走完，无论是文生图、图生图、换脸、倒推关键词等，都是走相同的流程。你们在实际开发过程中也可以参考我的项目来实现
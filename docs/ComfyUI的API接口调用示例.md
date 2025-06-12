ComfyUI的测试地址
本地comfyui测试地址：http://127.0.0.1:8188

POST /upload/mask
POST /upload/mask

上传蒙版图片接口，一般用于局部重绘

Body 请求参数

image: file://C:\Users\dourungeng\Pictures\640.png
type: input
subfolder: clipspace
original_ref: "{“filename”:”640.png”,”type”:”input”,”subfolder”:”clipspace”}"

AI写代码
yaml
1
2
3
4
5
请求参数
名称	位置	类型	必选	说明
body	body	object	否	none
» image	body	string(binary)	是	图片将以二进制格式发送到服务器
» type	body	string	否	上传图片的目标文件夹
» subfolder	body	string	否	上传图片的目标子文件夹
» original_ref	body	string	是	none
返回成功示例

{
  "name": "640.png",
  "subfolder": "clipspace",
  "type": "input"
}
AI写代码
json
1
2
3
4
5
返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
状态码 200

名称	类型	必选	约束	中文名	说明
» name	string	true	none		none
» subfolder	string	true	none		none
» type	string	true	none		none
POST /upload/image
POST /upload/image

上传图片接口

Body 请求参数

image: string

AI写代码
yaml
1
2
请求参数
名称	位置	类型	必选	说明
body	body	object	否	none
» image	body	string(binary)	是	图片将以二进制格式发送到服务器
返回成功示例

{
  "name": "0e9f-hiixpup5792613.jpg",
  "subfolder": "",
  "type": "input"
}
AI写代码
json
1
2
3
4
5
返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
状态码 200

名称	类型	必选	约束	中文名	说明
» name	string	true	none		none
» subfolder	string	true	none		none
» type	string	true	none		none
POST /prompt
POST /prompt

绘图任务的下发接口，此接口只做任务下发，返回任务ID信息。

Body 请求参数

{
  "client_id": "533ef3a3-39c0-4e39-9ced-37d290f371f8",
  "prompt": {
    "3": {
      "inputs": {
        "seed": 0,
        "steps": 20,
        "cfg": 2.5,
        "sampler_name": "euler",
        "scheduler": "karras",
        "denoise": 1,
        "model": [
          "14",
          0
        ],
        "positive": [
          "12",
          0
        ],
        "negative": [
          "12",
          1
        ],
        "latent_image": [
          "12",
          2
        ]
      },
      "class_type": "KSampler",
      "_meta": {
        "title": "K采样器"
      }
    },
    "8": {
      "inputs": {
        "samples": [
          "3",
          0
        ],
        "vae": [
          "15",
          2
        ]
      },
      "class_type": "VAEDecode",
      "_meta": {
        "title": "VAE解码"
      }
    },
    "12": {
      "inputs": {
        "width": 1024,
        "height": 576,
        "video_frames": 14,
        "motion_bucket_id": 32,
        "fps": 6,
        "augmentation_level": 0,
        "clip_vision": [
          "15",
          1
        ],
        "init_image": [
          "23",
          0
        ],
        "vae": [
          "15",
          2
        ]
      },
      "class_type": "SVD_img2vid_Conditioning",
      "_meta": {
        "title": "SVD_图像到视频_条件"
      }
    },
    "14": {
      "inputs": {
        "min_cfg": 1,
        "model": [
          "15",
          0
        ]
      },
      "class_type": "VideoLinearCFGGuidance",
      "_meta": {
        "title": "线性CFG引导"
      }
    },
    "15": {
      "inputs": {
        "ckpt_name": "svd_xt_1_1.safetensors"
      },
      "class_type": "ImageOnlyCheckpointLoader",
      "_meta": {
        "title": "Checkpoint加载器(仅图像)"
      }
    },
    "23": {
      "inputs": {
        "image": "C:\\Users\\dourungeng\\Pictures\\elephant1.png [input]",
        "upload": "image"
      },
      "class_type": "LoadImage",
      "_meta": {
        "title": "加载图像"
      }
    },
    "24": {
      "inputs": {
        "frame_rate": 6,
        "loop_count": 0,
        "filename_prefix": "SVD_img2vid",
        "format": "image/gif",
        "pingpong": false,
        "save_output": true,
        "images": [
          "8",
          0
        ]
      },
      "class_type": "VHS_VideoCombine",
      "_meta": {
        "title": "合并为视频"
      }
    }
  }
}
AI写代码
json

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
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
请求参数
名称	位置	类型	必选	说明
body	body	object	否	none
» client_id	body	string	是	none
» prompt	body	object	是	none
返回成功示例

{
  "prompt_id": "3604be44-eb6b-4d54-b82d-62d31a6c0b36",
  "number": 8,
  "node_errors": {}
}
AI写代码
json
1
2
3
4
5
返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
状态码 200

名称	类型	必选	约束	中文名	说明
» prompt_id	string	true	none		none
» number	integer	true	none		none
» node_errors	object	true	none		none
GET /prompt
GET /prompt

获取服务器当前剩余任务列队的数量

返回成功示例

{
  "exec_info": {
    "queue_remaining": 0
  }
}
AI写代码
json
1
2
3
4
5
返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
状态码 200

名称	类型	必选	约束	中文名	说明
» exec_info	object	true	none		none
»» queue_remaining	integer	true	none		none
GET /view
GET /view

图片的在线预览接口（上传图像，生图图像，蒙蔽图像，均通过该接口预览）

请求参数
名称	位置	类型	必选	说明
filename	query	string	是	图片名称
type	query	string	否	图片存放位置的文件夹（input为长传图片，output为生成的图片）
subfolder	query	string	否	子文件夹(没有可不填)
preview	query	string	否	预览
channel	query	string	否	none
返回示例

成功

返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
GET /queue
GET /queue

获取任务队列数量

返回示例

成功

{
  "queue_running": [],
  "queue_pending": []
}
AI写代码
json
1
2
3
4
返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
状态码 200

名称	类型	必选	约束	中文名	说明
» queue_running	[string]	true	none		none
» queue_pending	[string]	true	none		none
POST /queue
POST /queue

清除列队/无返回信息则为成功

Body 请求参数

{
  "clear": true
}
AI写代码
json
1
2
3
请求参数
名称	位置	类型	必选	说明
body	body	object	否	none
返回示例

200 Response

返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
POST /interrupt
POST /interrupt

取消当前任务/不需任何参数

返回示例

200 Response

返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
GET /history/{prompt_id}
GET /history/39d61fa4-58a4-4f61-a547-caab0f4c3a53

获取历史任务数据(根据任务prompt_id获取历史数据)

返回成功示例

{
  "39d61fa4-58a4-4f61-a547-caab0f4c3a53": {
    "prompt": [
      10,
      "39d61fa4-58a4-4f61-a547-caab0f4c3a53",
      {
        "3": {
          "inputs": {
            "seed": 687973405480854,
            "steps": 30,
            "cfg": 8,
            "sampler_name": "dpmpp_2m",
            "scheduler": "karras",
            "denoise": 1,
            "model": [
              "4",
              0
            ],
            "positive": [
              "6",
              0
            ],
            "negative": [
              "7",
              0
            ],
            "latent_image": [
              "5",
              0
            ]
          },
          "class_type": "KSampler",
          "_meta": {
            "title": "K采样器"
          }
        },
        "4": {
          "inputs": {
            "ckpt_name": "sdxl-动漫二次元_2.0.safetensors"
          },
          "class_type": "CheckpointLoaderSimple",
          "_meta": {
            "title": "Checkpoint加载器(简易)"
          }
        },
        "5": {
          "inputs": {
            "width": 512,
            "height": 512,
            "batch_size": 1
          },
          "class_type": "EmptyLatentImage",
          "_meta": {
            "title": "空Latent"
          }
        },
        "6": {
          "inputs": {
            "text": "1girl,flower,outdoors,solo,dress,long hair,closed eyes,sky,holding,smile,cloud,open mouth,field,blush,day,blue sky,white flower,holding flower,flower field,short sleeves,teeth,blue dress,petals,:d,facing viewer,grey hair,floating hair,wind,happy,^_^,daisy,upper teeth only,white dress,",
            "clip": [
              "4",
              1
            ]
          },
          "class_type": "CLIPTextEncode",
          "_meta": {
            "title": "CLIP文本编码器"
          }
        },
        "7": {
          "inputs": {
            "text": "(worst quality, low quality),deformed,distorted,disfigured,doll,poorly drawn,bad anatomy,wrong anatomy,",
            "clip": [
              "4",
              1
            ]
          },
          "class_type": "CLIPTextEncode",
          "_meta": {
            "title": "CLIP文本编码器"
          }
        },
        "8": {
          "inputs": {
            "samples": [
              "3",
              0
            ],
            "vae": [
              "4",
              2
            ]
          },
          "class_type": "VAEDecode",
          "_meta": {
            "title": "VAE解码"
          }
        },
        "9": {
          "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
              "8",
              0
            ]
          },
          "class_type": "SaveImage",
          "_meta": {
            "title": "保存图像"
          }
        }
      },
      {
        "client_id": "533ef3a3-39c0-4e39-9ced-37d290f371f8"
      },
      [
        "9"
      ]
    ],
    "outputs": {
      "9": {
        "images": [
          {
            "filename": "ComfyUI_00138_.png",
            "subfolder": "",
            "type": "output"
          }
        ]
      }
    },
    "status": {
      "status_str": "success",
      "completed": true,
      "messages": [
        [
          "execution_start",
          {
            "prompt_id": "39d61fa4-58a4-4f61-a547-caab0f4c3a53"
          }
        ],
        [
          "execution_cached",
          {
            "nodes": [],
            "prompt_id": "39d61fa4-58a4-4f61-a547-caab0f4c3a53"
          }
        ]
      ]
    }
  }
}
AI写代码
json

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
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
状态码 200

名称	类型	必选	约束	中文名	说明
» 39d61fa4-58a4-4f61-a547-caab0f4c3a53	object	true	none		下发任务prompt_id
»» prompt	[object]	true	none		下发任务的api工作流的原始提交参数
»» outputs	[object]	true	none		输出的结果
»» status	[object]	true	none		任务状态
GET /history
GET /history

获取历史任务列表

返回成功示例

{
    "d40751e8-3e96-472f-a818-90d36d06faf1": {
        "prompt": [
            0,
            "d40751e8-3e96-472f-a818-90d36d06faf1", {
                "3": {
                    "inputs": {
                        "seed": 0,
                        "steps": 30,
                        "cfg": 8,
                        "sampler_name": "dpmpp_2m",
                        "scheduler": "karras",
                        "denoise": 1,
                        "model": [
                            "4",
                            0
                        ],
                        "positive": [
                            "6",
                            0
                        ],
                        "negative": [
                            "7",
                            0
                        ],
                        "latent_image": [
                            "5",
                            0
                        ]
                    },
                    "class_type": "KSampler",
                    "_meta": {
                        "title": "K采样器"
                    }
                },
                "4": {
                    "inputs": {
                        "ckpt_name": "sdxl-动漫二次元_2.0.safetensors"
                    },
                    "class_type": "CheckpointLoaderSimple",
                    "_meta": {
                        "title": "Checkpoint加载器(简易)"
                    }
                },
                "5": {
                    "inputs": {
                        "width": 512,
                        "height": 512,
                        "batch_size": 1
                    },
                    "class_type": "EmptyLatentImage",
                    "_meta": {
                        "title": "空Latent"
                    }
                },
                "6": {
                    "inputs": {
                        "text": "1girl,flower,outdoors,solo,dress,long hair,closed eyes,sky,holding,smile,cloud,open mouth,field,blush,day,blue sky,white flower,holding flower,flower field,short sleeves,teeth,blue dress,petals,:d,facing viewer,grey hair,floating hair,wind,happy,^_^,daisy,upper teeth only,white dress,",
                        "clip": [
                            "4",
                            1
                        ]
                    },
                    "class_type": "CLIPTextEncode",
                    "_meta": {
                        "title": "CLIP文本编码器"
                    }
                },
                "7": {
                    "inputs": {
                        "text": "(worst quality, low quality),deformed,distorted,disfigured,doll,poorly drawn,bad anatomy,wrong anatomy,",
                        "clip": [
                            "4",
                            1
                        ]
                    },
                    "class_type": "CLIPTextEncode",
                    "_meta": {
                        "title": "CLIP文本编码器"
                    }
                },
                "8": {
                    "inputs": {
                        "samples": [
                            "3",
                            0
                        ],
                        "vae": [
                            "4",
                            2
                        ]
                    },
                    "class_type": "VAEDecode",
                    "_meta": {
                        "title": "VAE解码"
                    }
                },
                "9": {
                    "inputs": {
                        "filename_prefix": "ComfyUI",
                        "images": [
                            "8",
                            0
                        ]
                    },
                    "class_type": "SaveImage",
                    "_meta": {
                        "title": "保存图像"
                    }
                }
            }, {
                "extra_pnginfo": {
                    "workflow": {
                        "last_node_id": 9,
                        "last_link_id": 9,
                        "nodes": [{
                                "id": 5,
                                "type": "EmptyLatentImage",
                                "pos": [
                                    473,
                                    609
                                ],
                                "size": {
                                    "0": 315,
                                    "1": 106
                                },
                                "flags": {},
                                "order": 0,
                                "mode": 0,
                                "outputs": [{
                                        "name": "LATENT",
                                        "type": "LATENT",
                                        "links": "[Object]",
                                        "slot_index": 0,
                                        "label": "Latent"
                                    }
                                ],
                                "properties": {
                                    "Node name for S&R": "EmptyLatentImage"
                                },
                                "widgets_values": [
                                    512,
                                    512,
                                    1
                                ]
                            }, {
                                "id": 8,
                                "type": "VAEDecode",
                                "pos": [
                                    1209,
                                    188
                                ],
                                "size": {
                                    "0": 210,
                                    "1": 46
                                },
                                "flags": {},
                                "order": 5,
                                "mode": 0,
                                "inputs": [{
                                        "name": "samples",
                                        "type": "LATENT",
                                        "link": 7,
                                        "label": "Latent"
                                    }, {
                                        "name": "vae",
                                        "type": "VAE",
                                        "link": 8,
                                        "label": "VAE"
                                    }
                                ],
                                "outputs": [{
                                        "name": "IMAGE",
                                        "type": "IMAGE",
                                        "links": "[Object]",
                                        "slot_index": 0,
                                        "label": "图像"
                                    }
                                ],
                                "properties": {
                                    "Node name for S&R": "VAEDecode"
                                }
                            }, {
                                "id": 9,
                                "type": "SaveImage",
                                "pos": [
                                    1451,
                                    189
                                ],
                                "size": {
                                    "0": 210,
                                    "1": 58
                                },
                                "flags": {},
                                "order": 6,
                                "mode": 0,
                                "inputs": [{
                                        "name": "images",
                                        "type": "IMAGE",
                                        "link": 9,
                                        "label": "图像"
                                    }
                                ],
                                "properties": {},
                                "widgets_values": [
                                    "ComfyUI"
                                ]
                            }, {
                                "id": 4,
                                "type": "CheckpointLoaderSimple",
                                "pos": [
                                    26,
                                    474
                                ],
                                "size": {
                                    "0": 315,
                                    "1": 98
                                },
                                "flags": {},
                                "order": 1,
                                "mode": 0,
                                "outputs": [{
                                        "name": "MODEL",
                                        "type": "MODEL",
                                        "links": "[Object]",
                                        "slot_index": 0,
                                        "label": "模型"
                                    }, {
                                        "name": "CLIP",
                                        "type": "CLIP",
                                        "links": "[Object]",
                                        "slot_index": 1,
                                        "label": "CLIP"
                                    }, {
                                        "name": "VAE",
                                        "type": "VAE",
                                        "links": "[Object]",
                                        "slot_index": 2,
                                        "label": "VAE"
                                    }
                                ],
                                "properties": {
                                    "Node name for S&R": "CheckpointLoaderSimple"
                                },
                                "widgets_values": [
                                    "sdxl-动漫二次元_2.0.safetensors"
                                ]
                            }, {
                                "id": 6,
                                "type": "CLIPTextEncode",
                                "pos": [
                                    250,
                                    70
                                ],
                                "size": {
                                    "0": 422.84503173828125,
                                    "1": 164.31304931640625
                                },
                                "flags": {},
                                "order": 2,
                                "mode": 0,
                                "inputs": [{
                                        "name": "clip",
                                        "type": "CLIP",
                                        "link": 3,
                                        "label": "CLIP"
                                    }
                                ],
                                "outputs": [{
                                        "name": "CONDITIONING",
                                        "type": "CONDITIONING",
                                        "links": "[Object]",
                                        "slot_index": 0,
                                        "label": "条件"
                                    }
                                ],
                                "properties": {
                                    "Node name for S&R": "CLIPTextEncode"
                                },
                                "widgets_values": [
                                    "1girl,flower,outdoors,solo,dress,long hair,closed eyes,sky,holding,smile,cloud,open mouth,field,blush,day,blue sky,white flower,holding flower,flower field,short sleeves,teeth,blue dress,petals,:d,facing viewer,grey hair,floating hair,wind,happy,^_^,daisy,upper teeth only,white dress,"
                                ]
                            }, {
                                "id": 7,
                                "type": "CLIPTextEncode",
                                "pos": [
                                    340,
                                    290
                                ],
                                "size": {
                                    "0": 425.27801513671875,
                                    "1": 180.6060791015625
                                },
                                "flags": {},
                                "order": 3,
                                "mode": 0,
                                "inputs": [{
                                        "name": "clip",
                                        "type": "CLIP",
                                        "link": 5,
                                        "label": "CLIP"
                                    }
                                ],
                                "outputs": [{
                                        "name": "CONDITIONING",
                                        "type": "CONDITIONING",
                                        "links": "[Object]",
                                        "slot_index": 0,
                                        "label": "条件"
                                    }
                                ],
                                "properties": {
                                    "Node name for S&R": "CLIPTextEncode"
                                },
                                "widgets_values": [
                                    "(worst quality, low quality),deformed,distorted,disfigured,doll,poorly drawn,bad anatomy,wrong anatomy,"
                                ]
                            }, {
                                "id": 3,
                                "type": "KSampler",
                                "pos": [
                                    863,
                                    186
                                ],
                                "size": {
                                    "0": 315,
                                    "1": 262
                                },
                                "flags": {},
                                "order": 4,
                                "mode": 0,
                                "inputs": [{
                                        "name": "model",
                                        "type": "MODEL",
                                        "link": 1,
                                        "label": "模型"
                                    }, {
                                        "name": "positive",
                                        "type": "CONDITIONING",
                                        "link": 4,
                                        "label": "正面条件"
                                    }, {
                                        "name": "negative",
                                        "type": "CONDITIONING",
                                        "link": 6,
                                        "label": "负面条件"
                                    }, {
                                        "name": "latent_image",
                                        "type": "LATENT",
                                        "link": 2,
                                        "label": "Latent"
                                    }
                                ],
                                "outputs": [{
                                        "name": "LATENT",
                                        "type": "LATENT",
                                        "links": "[Object]",
                                        "slot_index": 0,
                                        "label": "Latent"
                                    }
                                ],
                                "properties": {
                                    "Node name for S&R": "KSampler"
                                },
                                "widgets_values": [
                                    0,
                                    "randomize",
                                    30,
                                    8,
                                    "dpmpp_2m",
                                    "karras",
                                    1
                                ]
                            }
                        ],
                        "links": [
                            [
                                1,
                                4,
                                0,
                                3,
                                0,
                                "MODEL"
                            ],
                            [
                                2,
                                5,
                                0,
                                3,
                                3,
                                "LATENT"
                            ],
                            [
                                3,
                                4,
                                1,
                                6,
                                0,
                                "CLIP"
                            ],
                            [
                                4,
                                6,
                                0,
                                3,
                                1,
                                "CONDITIONING"
                            ],
                            [
                                5,
                                4,
                                1,
                                7,
                                0,
                                "CLIP"
                            ],
                            [
                                6,
                                7,
                                0,
                                3,
                                2,
                                "CONDITIONING"
                            ],
                            [
                                7,
                                3,
                                0,
                                8,
                                0,
                                "LATENT"
                            ],
                            [
                                8,
                                4,
                                2,
                                8,
                                1,
                                "VAE"
                            ],
                            [
                                9,
                                8,
                                0,
                                9,
                                0,
                                "IMAGE"
                            ]
                        ],
                        "groups": [],
                        "config": {},
                        "extra": {
                            "ds": {
                                "scale": 1,
                                "offset": {
                                    "0": 858,
                                    "1": 196
                                }
                            }
                        },
                        "version": 0.4,
                        "widget_idx_map": {
                            "3": {
                                "seed": 0,
                                "sampler_name": 4,
                                "scheduler": 5
                            }
                        }
                    }
                },
                "client_id": "a4ff6051dabe4c7d994460b62c6c8f14"
            },
            [
                "9"
            ]
        ],
        "outputs": {
            "9": {
                "images": [{
                        "filename": "ComfyUI_00131_.png",
                        "subfolder": "",
                        "type": "output"
                    }
                ]
            }
        },
        "status": {
            "status_str": "success",
            "completed": true,
            "messages": [
                [
                    "execution_start", {
                        "prompt_id": "d40751e8-3e96-472f-a818-90d36d06faf1"
                    }
                ],
                [
                    "execution_cached", {
                        "nodes": [],
                        "prompt_id": "d40751e8-3e96-472f-a818-90d36d06faf1"
                    }
                ]
            ]
        }
    }
}

返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
状态码 200

名称	类型	必选	约束	中文名	说明
» d40751e8-3e96-472f-a818-90d36d06faf1	object	true	none		none
»» prompt	[object]	true	none		none
»» outputs	[object]	true	none		none
»» status	[object]	true	none		none
GET /system_stats
GET /system_stats

系统统计信息接口

返回成功示例

{
  "system": {
    "os": "nt",
    "python_version": "3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)]",
    "embedded_python": false
  },
  "devices": [
    {
      "name": "cuda:0 NVIDIA GeForce RTX 4070 Ti SUPER : cudaMallocAsync",
      "type": "cuda",
      "index": 0,
      "vram_total": 17170956288,
      "vram_free": 15702425600,
      "torch_vram_total": 67108864,
      "torch_vram_free": 33554432
    }
  ]
}

返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
状态码 200

名称	类型	必选	约束	中文名	说明
» system	object	true	none		none
»» os	string	true	none		none
»» python_version	string	true	none		none
»» embedded_python	boolean	true	none		none
» devices	[object]	true	none		none
»» name	string	false	none		none
»» type	string	false	none		none
»» index	integer	false	none		none
»» vram_total	integer	false	none		none
»» vram_free	integer	false	none		none
»» torch_vram_total	integer	false	none		none
»» torch_vram_free	integer	false	none		none
GET /object_info/{node_class}
GET /object_info/KSampler

根据组件名称获取系统中组件参数

返回示例
成功

{
  "KSampler": {
    "input": {
      "required": {
        "model": [
          "MODEL"
        ],
        "seed": [
          "INT",
          {
            "default": 0,
            "min": 0,
            "max": 18446744073709552000
          }
        ],
        "steps": [
          "INT",
          {
            "default": 20,
            "min": 1,
            "max": 10000
          }
        ],
        "cfg": [
          "FLOAT",
          {
            "default": 8,
            "min": 0,
            "max": 100,
            "step": 0.1,
            "round": 0.01
          }
        ],
        "sampler_name": [
          [
            "euler",
            "euler_ancestral",
            "heun",
            "heunpp2",
            "dpm_2",
            "dpm_2_ancestral",
            "lms",
            "dpm_fast",
            "dpm_adaptive",
            "dpmpp_2s_ancestral",
            "dpmpp_sde",
            "dpmpp_sde_gpu",
            "dpmpp_2m",
            "dpmpp_2m_sde",
            "dpmpp_2m_sde_gpu",
            "dpmpp_3m_sde",
            "dpmpp_3m_sde_gpu",
            "ddpm",
            "lcm",
            "ddim",
            "uni_pc",
            "uni_pc_bh2"
          ]
        ],
        "scheduler": [
          [
            "normal",
            "karras",
            "exponential",
            "sgm_uniform",
            "simple",
            "ddim_uniform"
          ]
        ],
        "positive": [
          "CONDITIONING"
        ],
        "negative": [
          "CONDITIONING"
        ],
        "latent_image": [
          "LATENT"
        ],
        "denoise": [
          "FLOAT",
          {
            "default": 1,
            "min": 0,
            "max": 1,
            "step": 0.01
          }
        ]
      }
    },
    "output": [
      "LATENT"
    ],
    "output_is_list": [
      false
    ],
    "output_name": [
      "LATENT"
    ],
    "name": "KSampler",
    "display_name": "KSampler",
    "description": "",
    "category": "sampling",
    "output_node": false
  }
}

返回结果
状态码	状态码含义	说明	数据模型
200	OK	成功	Inline
返回数据结构
状态码 200

名称	类型	必选	约束	中文名	说明
» KSampler	object	true	none		none
»» input	object	true	none		none
»»» required	object	true	none		none
»»»» model	[string]	true	none		none
»»»» seed	[object]	true	none		none
关
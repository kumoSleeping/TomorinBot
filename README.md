

<h1 align="center"> TomorinBOT  <img src="http://q1.qlogo.cn/g?b=qq&nk=211134009&s=100" width="30" height="30" alt="tmrn"/> </h1>


<p align="center">


<a href="https://github.com/kumoSleeping/TomorinBot/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/kumoSleeping/TomorinBot" alt="license">
  </a>
<a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.9+-blue?logo=python&logoColor=edb641" alt="license">
  </a>

  <a href="https://satori.js.org/zh-CN/">
    <img src="https://img.shields.io/badge/Satori-v1-black?style=social">
  </a>


***
## 📖 介绍

> 你现在看到的 `satomori` 分支是基于 `satori-python` 的小工具包。

> Based on -> [satori-python](https://github.com/RF-Tar-Railt/satori-python/blob/main/docs.md) 
## 💫 快速起航

```shell
pip install satori-python
```

```shell
python tmrn
```



## 📚 编写前的准备

打开 `tmrn/__main__.py` 文件，你会看到这样的代码：

```python
from satori.client import WebsocketsInfo
from tmrn.__init__ import app

import bar  # 导入插件

# app.apply(
#     WebsocketsInfo(
#     ...
#     )
# )

```

`app` 是一个 `App` 类的实例，此处用于注册连接信息。   
`import bar` 是导入模块的示例，与 `tmrn` 文件夹同级。


## 📂 简单插件

```py
from satori import Event, WebsocketsInfo, EventType
from satori.element import E
from satori.client import Account, App
from tmrn import app, cmd_select


# 注册
@app.register_on(EventType.MESSAGE_CREATED)
async def on_message_(account: Account, event: Event):
    if msg := cmd_select(event, prefix=['/', '']):
        if msg == 'ping':
            send_msg = E.text('pong').dumps()

            # from PIL import Image
            # import io
            # img = Image.new('RGB', (100, 100), color='red')
            # img_bytes = io.BytesIO()
            # img.save(img_bytes, format='PNG')
            # send_msg += E.image(raw=img_bytes, mime='image/png').dumps()

            # 发送消息
            await account.send(event, send_msg)
```
本例中，我们定义了一个简单的插件，当收到消息时，如果消息是 `/ping`，则回复 `pong`。
注释部分是发送图片的示例，你可以取消注释并将图片发送到聊天中。

## 🔧 实用工具

### `log` 日志对象

`log` 对象用于输出日志。

- `info` 方法: 输出信息日志
- `error` 方法: 输出错误日志
- `warning` 方法: 输出警告日志
- `debug` 方法: 输出调试日志
- `success` 方法: 输出成功日志

`c` 用于输出彩色 `ANSI` 转义颜色。

此模块利用 ANSI 转义序列实现，在最新的 Windows cmd 中，我们尝试使用 `os.system('')` 唤醒 ANSI 支持。


### `cmd_select` 命令文本选择器


> 用于在在合适的时候获取适合于命令的纯文本信息

- 当消息中有 at 时，如果at的是bot，返回 pure_text，否则返回 None
- 当消息中有引用时，如果引用的是bot，返回 pure_text，否则返回 None
- 当 prefix 被规定时，如果消息以 prefix 开头，返回 pure_text，否则返回 None，如果是 '' 空字符串，任何消息都会触发
- 如果 white_user 被规定时，消息发送者在 white_user 中才会触发，否则不会触发

使用方法详见函数注释。

## 📜 许可证

`Tomorin` 使用 `MIT` 许可证。查看 [LICENSE](https://github.com/kumoSleeping/TomorinBot/blob/main/LICENSE) 文件了解更多信息。


## 📄 关于

`satori-python` 是一个基于 `satori` 协议的 `SDK` 。  
原本的 `tmrn` 设计思路在很多方面与 `satori-python-client` 有很多相像，但很明显，`satori-python-client` 更加完善。
我早就知道这是同一条赛道上不可能赢的竞争，但我总有自己喜欢的方式。
你现在看到的就是 ~~(我完全投入了rf的怀抱)~~ 。

    有能做到的事，也就一定有做不到的事情。

本模版出发点是学习与探索设计方法，让简单的功能实现可以高速产出。   

`Tomorin` 追求方便快捷，符合舒心机器人标准的开发工具。一直在学习与向前，感谢一路陪伴与支持。








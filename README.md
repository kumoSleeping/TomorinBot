

<h1 align="center"> TomorinBOT  <img src="http://q1.qlogo.cn/g?b=qq&nk=211134009&s=100" width="30" height="30" alt="tmrn"/> </h1>


<p align="center">

<a href="https://github.com/kumoSleeping/TomorinBot/blob/main/core/__init__.py">
    <img src="https://img.shields.io/badge/TomorinBOT%20v5-blue" alt="license">
  </a>

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


`Tomorin` 是一个基于 [Satori协议](https://satori.js.org/zh-CN/) 的家用异步聊天机器人框架。
使用装饰器标记函数，使得在收到各类信息时或指定状态时，对应函数被调用。

## 💫 快速起航

`Tomorin` 非常注重依赖的的轻小，你只需要安装 `satori-python-core` 与 `aiohttp` 即可运行。

```shell
pip install satori-python-core aiohttp
```

```shell
python -m core
```


首次运行时会生成一个 `config.json` 文件，你需要主动关闭应用，在其中填写你的合适的配置后重启以加载新的配置。


## 📚 编写前的准备

在 `Tomorin` 中，`core` 会导入同目录下的 `Python` 模块（module）。

它可以是一个 `.py` 文件

    📜 foo.py
    
也可以是一个包含 `__init__.py` 的文件夹。 

    📂 bar   
    └── 📜 __init__.py   

按照常规聊天机器人框架的叫法，我们可以叫它为插件，尽管目前它还什么都没做。要想做到在某种情况下调用函数，请看 `on` 装饰器。

## 📂 简单插件

```py
from core.interfaces import Event, on


@on.message_created
async def echo_(event: Event):
    if (r := event.message.content).startswith('echo '):
        await event.message_create(r[5:])

```
本例中，`on.message_created` 是一个装饰器，用于注册一个函数，当 bot 收到 message-created 事件时调用。   
在大家都很熟悉的 `satori` 协议中，`message-created` 事件是指收到了一条消息。
紧接着我们判断消息是否以 `echo ` 开头，如果是，我们就将消息内容去除前五个字符后，使用 `event.message_create` 方法发送消息。

## 🔌 `core interfaces`

`core` 模块提供了一些接口，用于功能的编写。

```py
from core.interfaces import Event, on, config, log, initialize_manager
```

### `Event` 事件对象

在收到 `satori` 资源推送时，会被 parse 成一个 `Event` 对象，来自 `saotri-python-core`，同时提供了发送 **标准事件** 方法。

例如上面的例子中，`event.message_create` 即是一个标准事件方法，同时支持自动判断同步与异步的调用。


### `on` 装饰器

`on` 装饰器用于注册一个函数，当 bot 收到对应事件时调用。
例如上面的例子中，`on.message_created` 即是一个装饰器，用于注册一个函数，当 bot 收到 message-created 事件时调用。
此外还提供了三种 `bot` 装饰器。 
- `on.bot_start_up`: bot 启动后调用
- `on.bot_event_built`: bot 事件构建完成后调用
- `on.bot_api_requested`: bot 请求 api 时的事件完成(标准事件发送成功)后调用

### `config` 配置对象

`config` 对象用于操作配置文件中的配置项。

- `need` 方法: 声明在配置文件需要一个此项，并会在不存在时创建并填入默认值，创建成功后自动重载配置文件。
- `get_key` 方法: 获取配置文件中的配置项的值。

### `log` 日志对象

`log` 对象用于输出日志。

- `info` 方法: 输出信息日志
- `error` 方法: 输出错误日志
- `warning` 方法: 输出警告日志
- `debug` 方法: 输出调试日志
- `success` 方法: 输出成功日志

`c` 用于输出彩色 `ANSI` 转义颜色。

此模块利用 ANSI 转义序列实现，在最新的 Windows cmd 中，我们尝试使用 `os.system('')` 唤醒 ANSI 支持。

### initialize_manager 

`initialize_manager` 用于初始化插件 / 注册管理器。


## 🧭 同步代码迁移

`Tomorin` 从 `v4` 迁移到 `v5` 时，进行了一些重大的变更，从多线程到异步的转变使得插件的编写方式发生了一些变化。
在重构的同时，我们可以使用多线程来还原原本的插件编写方式。

```py
from core.interfaces import Event, on
import threading
import asyncio
import time


@on.message_created
async def sync_test(event: Event):

    def test(event: Event):
        if event.message.content == '.t':
            time.sleep(10)
            event.message_create('sync')

    threading.Thread(target=test, args=(event,),daemon=True).start()


@on.message_created
async def async_test(event: Event):
    if event.message.content == '.t':
        await asyncio.sleep(10)
        await event.message_create('async')
```

上面的例子中，`sync_test` 使用闭包的方式，直接迁移 `v4` 的同步函数到 `v5`。

> `event.message_create` 等标准事件方法简单的自动判断了同步与异步的调用，这种方法本质是为了避免阻塞。
 

## 📜 许可证

`Tomorin` 使用 `MIT` 许可证。查看 [LICENSE](https://github.com/kumoSleeping/TomorinBot/blob/main/LICENSE) 文件了解更多信息。


## 📄 关于
> 有框架能做到的事，也就一定有框架做不到的事情。

本模版出发点是学习与探索设计方法，让简单的功能实现可以高速产出。   

`Tomorin` 追求不过度、不刻意、不耦合。   
一直在学习与向前，感谢一路陪伴与支持。










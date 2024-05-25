

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


`Tomorin` 是一个基于 [Satori协议](https://satori.js.org/zh-CN/) 的迷你家用聊天机器人框架。
使用装饰器标记函数，使得在收到各类信息时或指定状态时，对应函数被调用。

## 💫 快速起航

```shell
pip install satori-python-core aiohttp
```

```shell
python -m core
```

~~可以使用 `hupper` 来实现热重启。~~


首次运行时会生成一个 `config.json` 文件，你需要主动关闭应用，在其中填写你的合适的配置后重启以加载新的配置。

## 📊 异步与同步(多线程)支持

`Tomorin` 是一个异步框架。  

`asyncio.create_task` 位于主线程，可以放心使用诸如 `Alconna` 等使用了 `contextvars` 的库而不会出现线程错误问题。

**同步(多线程)支持**

在收到消息推送时，常规异步事件循环之外，会独立的创建一个新的线程支持注册的同步函数。`event` 的 标准事件函数也做了相应适配。

>设置 `config.json` `support_sync` 为 `False` 可以关闭同步支持。


## 📚 插件编写前的准备

在正式编写插件之前，我们需要先了解一下插件的概念。


在 `Tomorin` 中，插件即是 `Python` 的一个模块（module）。
`Tomorin` 会使得他们被导入。插件间应尽量减少耦合，可以进行有限制的相互调用。

一个普通的 `.py` 文件即可以作为一个插件，例如创建一个 `foo.py` 文件：
```
📜 foo.py
```
这个时候模块 `foo` 已经可以被称为一个插件了，尽管它还什么都没做。

一个包含 `__init__.py` 的文件夹即是一个常规 `Python` 包 `package`，例如创建一个 `foo` 文件夹：
```
📂 foo   
└── 📜 __init__.py   
```
这个时候包 `foo` 同样是一个合法的插件，插件内容可以在 `__init__.py` 文件中编写，例如项目代码中的 `rec` 插件。

但 `Tomorin` 的插件也只起到被导入的作用，而要做到在某种情况下调用函数，请看 `on` 装饰器。

## 📂 简单插件

```py
from core.interfaces import Event, on

# 异步
@on.message_created
async def echo_(event: Event):
    if (r := event.message.content).startswith('echo '):
        await event.message_create(r[5:])
        
# 同步
@on.message_created
def echo2(event: Event):
    if (r := event.message.content).startswith('echo2 '):
        event.message_create(r[6:])
```
> 本例中，`on.message_created` 是一个装饰器，用于注册一个函数，当 bot 收到 message-created 事件时调用。两个函数会被同时以 多线程 与 异步 的方式调用。

- 利用来自 `core` 的 `config` 实现资源配置


## 🔌 core interfaces

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
 

## 📜 许可证

`Tomorin` 使用 `MIT` 许可证。查看 [LICENSE](https://github.com/kumoSleeping/TomorinBot/blob/main/LICENSE) 文件了解更多信息。

## 📄 关于
> 有框架能做到的事，也就一定有框架做不到的事情。

本模版出发点是学习与探索设计方法，让简单的功能实现可以高速产出。   

`Tomorin` 追求不过度、不刻意、不耦合。   
一直在学习与向前，感谢一路陪伴与支持。










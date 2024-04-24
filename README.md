

<h1 align="center"> TomorinBOT  <img src="http://q1.qlogo.cn/g?b=qq&nk=211134009&s=100" width="30" height="30" alt="tmrn"/> </h1>


<p align="center">

<a href="https://github.com/kumoSleeping/TomorinBot/blob/main/core/__init__.py">
    <img src="https://img.shields.io/badge/TomorinBOT%20v3-blue" alt="license">
  </a>

<a href="https://github.com/kumoSleeping/TomorinBot/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/kumoSleeping/TomorinBot" alt="license">
  </a>
<a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.7+-blue?logo=python&logoColor=edb641" alt="license">
  </a>

  <a href="https://satori.js.org/zh-CN/">
    <img src="https://img.shields.io/badge/Satori-v1-black?style=social">
  </a>



***
## 介绍


`Tomorin` 使用 **同步编程** + **线程**，通过函数的**注册**完成功能的规划，基于 [Satori协议](https://satori.js.org/zh-CN/) 构建简单的 **河流形** 聊天机器人后端。

> **河流形** 指的是消息的流动，消息从上游流向下游，中间经过各种处理后，在被抽象成 `Event` 事件后分为众多支流 (例如每个插件是一条支流) 。

用户可以在此模版上使用 `mods.on.xxx` 装饰器进行标记自己的函数，使得在收到各类信息时，对应函数被调用。
- 支流类事件: `internal` 和各种 [标准事件](https://satori.js.org/zh-CN/resources/message.html#%E4%BA%8B%E4%BB%B6)（例如message_created，friend_request等） 会在 `Event` 事件后被分发且都会开启新的线程进行处理。   
- 干流类事件: `before_event`, `after_request` 等等，属于干流类事件，会在 `Event` 事件被分发前调用，且会按照优先级同步等待数据处理结束后再继续。


```shell
pip install requests websocket-client
```

```shell
python3 -m core
```

## 关于
本模版出发点是学习与探索设计方法，让简单的功能实现可以高速产出。   
`.gitignore`规则了忽视了一些东西，请注意检查。

## 为什么不使用异步编程
本项目存在异步版本的分支 `Tomorin BOT Async`，但是使用时明显感受到心智负担的增加。   
对于初学者来说，异步的学习曲线是很陡的，而简单的功能同步编程较为舒适，功能优化一般也是否异步无关的。  
在测试了一段时间的 `Tomorin BOT Async` 后，即使一定压力下功能符合预期，但我依然认为 `Python` 机器人项目下异步对我来说没有优势，故不用。   
`Tomorin BOT Async` 会在完善后开源 (大概) 。


## docs


本项目只需要 `./core` 即可运行，通常第一次运行时会生成一个 `config.json` 文件，你需要主动关闭应用，在其中填写你的合适的配置。

你可以使用 `hupper` 来实现热重启。

```shell
pip install hupper
```

```shell
hupper -m core
```


## 插件

`core` 是 tmrn 的核心，`core` 甚至可以不依赖成型的 `mods` 与 `plugs` 运行 bot 。

`mods` 模块从 `core` 导入了需要的函数、方法作为依赖，并扩展了各种工具。你也可以在其中写入你的模块包，然后在 `mods/__init__.py` 中引入。    

`plugs` 模块会被`core` 引入为插件，你可以在其中 `__init__.py` 写入你的的一个功能，也可以单独在此包内建立子模块并导入。   


```py
# 使用字符串处理
import mods

@mods.on.message_created
def echo_(event: mods.Event):
    if (r := event.message.content).startswith('echo '):
        event.message_create(r[5:])
```

```py
# 使用 match_command 扩展
import mods

@mods.on.message_created
def echo_(event: mods.Event):
    if res := mods.match_command(event, 'echo'):
        res.send(res.text)
```


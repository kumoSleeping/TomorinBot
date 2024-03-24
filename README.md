

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


Tomorin是由Python编写的，结构简单、客户端低代码量、使用同步编程+线程化、使用注册+模块思想，基于**Satori协议**的**聊天机器人后端模版**。     
因此，本程序也是一个satori协议的客户端实现，用于连接satori服务器，接收和发送消息。   
用户可以在此模版上编写注册自己的函数，使得在收到各类信息时，对应函数被调用。    

## 运行

```shell
pip install requests websocket-client
```

```shell
python3 -m core
```

> 通常第一次运行时会生成一个 `config.json` 文件，你需要主动关闭应用，在其中填写你的合适的配置。

你可以使用 `hupper` 来实现热重启。

```shell
pip install hupper
```

```shell
hupper -m core
```


## 关于开发

基于[Satori协议](https://satori.js.org/zh-CN/)的快速上手。


```py
from mods import on, Event

@on.message_created
def echo_(event: Event):
    if (r := event.message.content).startswith('echo '):
        event.message_create(r[5:])
```

简单的快速开发。



## 关于
本模版出发点是学习与探索设计方法，让简单的功能实现可以高速产出。   
`.gitignore`规则了忽视了一些东西，请注意检查。


------




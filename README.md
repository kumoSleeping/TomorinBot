

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


`Tomorin` 使用 **同步编程** + **线程** 开发core、插件、依赖，对其数据 **注册** **依赖** **分发**，基于 [Satori协议](https://satori.js.org/zh-CN/) 构建简单的 **河流形** 聊天机器人后端、协议客户端。

**河流形** 指的是消息的流动，消息从上游流向下游，中间经过各种处理后，在被抽象成 `Event` 事件后分为众多支流。

用户可以在此模版上使用 `on.xxx` 装饰器进行标记自己的函数，使得在收到各类信息时，对应函数被调用。
- 支流类事件: `internal` 和各种 [标准事件](https://satori.js.org/zh-CN/resources/message.html#%E4%BA%8B%E4%BB%B6)（例如message_created，friend_request等） 会在 `Event` 事件后被分发且都会开启新的线程进行处理。   
- 干流类事件: `before_event`, `after_request` 等等，属于干流类事件，会在 `Event` 事件被分发前调用，且会按照优先级同步等待数据处理结束后再继续。

本项目简单容易理解。但缺点也显而易见，**不适用**大型项目、高量级并发、复杂功能。 

`Nonebot2` 与 `Koishi` 依然是机器人构建的最佳实践。

## 运行

```shell
pip install requests websocket-client
```

```shell
python3 -m core
```


## 关于
本模版出发点是学习与探索设计方法，让简单的功能实现可以高速产出。   
`.gitignore`规则了忽视了一些东西，请注意检查。

## 文档 (画重点！)

- [ ] [Satori文档](https://satori.js.org/zh-CN/)
- [ ] [本框架文档](docs/)
- [ ] [Koishi文档(参考)](https://koishi.chat/zh-CN/)


------




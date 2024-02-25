


[//]: # (<h1 align="center"> TomorinBOT  <img src="./DemoProject2/register/example/eg.jpg" width="30" height="30" alt="tmrn"/> </div></h1>)
<h1 align="center"> TomorinBOT  <img src="http://q1.qlogo.cn/g?b=qq&nk=211134009&s=100" width="30" height="30" alt="tmrn"/> </div></h1>


<p align="center">

<a href="https://github.com/kumoSleeping/TomorinBot/blob/main/core/__init__.py#L8C1-L8C22">
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

</p>
<p align="center">
<br>  かつて忘れられない、星空は未来を照らし、次の春へ。
<br>
――「2024.1.30 10:54:23・東京・豊島区」
<br> 

***
## 介绍


Tomorin是由Python编写的，结构简单、客户端低代码量、使用同步编程+线程化、使用注册+模块思想，基于**Satori协议**的**聊天机器人后端模版**。     
因此，本程序也是一个satori协议的客户端实现，用于连接satori服务器，接收和发送消息。   
用户可以在此模版上编写注册自己的函数，使得在收到各类信息时，对应函数被调用。    

## 安装 core 所需依赖

```shell
pip install PyYAML requests hupper websocket-client
```

## 运行

```shell
python3 core
```

## core


```mermaid

classDiagram
    class core { 
    }

    class loader{
        记录注册的函数
    }
    class transmit{
        与服务端进行satori协议通讯
    }
    class on{
        提供用于注册各种事件的装饰器
    }
    class main{
        接收通讯数据
        将数据加工为event对象
        为注册的函数分发event
    }
    class app{
        <<启动项目>>
        调用loader
    }

    class event{
        将接收到的数据加工为event对象
    }

    __init__ -- core : 对外提供接口
    loader -- core : 记录注册
    transmit -- core : 发送请求、注册
    on -- core : 事件、注册装饰器
    main -- core : 数据接收、注册
    app -- core : 启动项目
    event -- core : 提供基础属性、方法


```





## 关于此模版
本模版出发点是学习与探索设计方法，让简单的功能实现可以高速产出。 


如果您习惯使用SDK编写项目，推荐您使用[RF-Tar-Railt/satori-python](https://github.com/RF-Tar-Railt/satori-python/releases/tag/v0.4.0)进行开发。

## 仓库
`.gitignore`规则了忽视了一些东西，请注意检查。


------




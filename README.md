

<h1 align="center"> TomorinBOT  <img src="http://q1.qlogo.cn/g?b=qq&nk=211134009&s=100" width="30" height="30" alt="tmrn"/> </h1>


<p align="center">

<a href="https://github.com/kumoSleeping/TomorinBot/blob/main/core/__init__.py">
    <img src="https://img.shields.io/badge/TomorinBOT%20v4-blue" alt="license">
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

## 关于
本模版出发点是学习与探索设计方法，让简单的功能实现可以高速产出。   
`.gitignore`规则了忽视了一些东西，请注意检查。

**为什么不使用异步编程?**   

本项目存在异步版本的分支 `Tomorin BOT Async`，但是使用时明显感受到心智负担的增加。   
对于初学者来说，异步的学习曲线是很陡的，而简单的功能同步编程较为舒适，功能优化一般也是否异步无关的。  
在测试了一段时间的 `Tomorin BOT Async` 后，即使一定压力下功能符合预期，但我依然认为 `Python` 机器人项目下异步对我来说没有优势，故不用。   
`Tomorin BOT Async` 会在完善后开源 (大概) 。

## 项目结构

### core

`core` 是 tmrn 的核心，提供了必要工具与运行流程。
> `core` 包含 `classes`、`transmit` 文件夹，以及 `__init__` 与 `__main__` 脚本。

#### __init__.py
只包含一个版本号识别，用于识别为包.

#### __main__.py
项目启动运行 `initialize`:

1.加载 `plugs` 所有插件   
2.执行所有 `on.bot_start_up` 事件   
3.启动 `transmit` 传输类的 `bot_websocket`   

#### transmit
`transmit` 文件夹内的 `bot_http` `bot_websocket` 为 `satori` 协议的 `http` `websocket` 传输类。`tmrn` 与 `satori` 协议绑定，因此 `http` `websocket` 格式已与 `satori` 协议保持一致。   
这两个脚本同时包含了 `event` 从消息触发构建，到结束的全部流程。

#### `classes`
`classes` 类中有必须的类，还请查看。

### mods
`mods` 模块从 `core` 导入了需要的函数、方法作为依赖，并扩展了各种工具。你也可以在其中写入你的模块包，然后在 `mods/__init__.py` 中引入。    

### plugs
`plugs` 模块会被`core` 引入为插件，你可以在其中 `__init__.py` 写入你的的一个功能，也可以单独在此包内建立子模块并导入。   



## 运行

```shell
pip install requests websocket-client
```

```shell
python -m core
```

你可以使用 `hupper` 来实现热重启。

```shell
pip install hupper
```

```shell
hupper -m core
```

本项目第一次运行时会生成一个 `config.json` 文件，你需要主动关闭应用，在其中填写你的合适的配置后重启以加载新的配置。


```
 ----------------------------------------------------------------- 
| TomorinBOT - v4.3.0 - @2023-2024 Compliant with Satori Protocol |
 ----------------------------------------------------------------- 
● 18:51:12 [TomorinBot-core] > load registry...
● 18:51:12 [TomorinBot-core] IDX     FUNCTION NAME      ATTRIBUTES_TAG
● 18:51:12 [TomorinBot-core] ---     -------------      --------------
● 18:51:12 [TomorinBot-core] (1)     display_receive    bot:event-built
● 18:51:12 [TomorinBot-core] (2)     display_send       bot:api-requested
● 18:51:12 [TomorinBot-core] (3)     echo               message-created
● 18:51:12 [TomorinBot-core] (4)     refresh_data       bot:start-up
● 18:51:13 [TomorinBot-core] ✓ load registry complete.
● 18:51:13 [TomorinBot-core] > bot:started function started...
● 18:51:13 [mods-schedule_do] refresh_data is scheduled for every 86400 seconds.
● 18:51:13 [TomorinBot-core] ✓ bot:started function <refresh_data> executed.
● 18:51:13 [TomorinBot-core] ✓ bot:started function completed.
● 18:51:13 [core-transmit] > link start...
● 18:51:13 [core-transmit] ✓ Satori driver connected.
● 18:51:13 [core-transmit] [] login [chronocat]
● 18:51:13 [mods-schedule_do] Do <function refresh_data at 0x139f6f920> now!
● 18:51:15 [TomorinBot-core] かつて忘れられない、星空は未来を照らし、次の春へ。    ―― 2024.1.30 10:54:23・東京・豊島区

Process finished with exit code 143 (interrupted by signal 15:SIGTERM)
```



## 快速上手


下面的例子可以直接写在 `mods/__init__.py` 中，也可以在 `plugs` 中建立一个模块包，然后在 `plugs/__init__.py` 中引入。

> 最简单的 `echo` 插件
```py
import mods

@mods.on.message_created
def echo_(event: mods.Event):
    if (r := event.message.content).startswith('echo '):
        event.message_create(r[5:])
```

> 使用 match_command 扩展实现一个 `echo` 命令
```py
import mods

@mods.on.message_created
def echo_(event: mods.Event):
    if res := mods.match_command(event, 'echo', limit_admin=True, allow_gap_less=True):
        res.send(res.text)
```

>使用来自 `core` 的  `assets` 与来自 `mods` 的  `h` 在入群时发送一张图片
```py
import mods

path = mods.assets('cat.jpg')
with open(path, 'rb') as f:
    cat_pic = f.read()

@mods.on.guild_member_added
def a_cat(event: mods.Event):
    if event.guild.id == 1234567890:
        event.message_create(f'Welcome {event.user.name}!{mods.h.image(cat_pic, 'cat.jpg')}')
```

> 使用来自 `mods` 的 定时器 与 间隔器 实现常规定时任务   
> 请注意，定时器与间隔器的时间单位为秒，且定时器会在启动时立即执行一次，可以通过 `do_now` 参数控制是否立即执行。   
> 通过 `@mods.on.bot_start_up` 装饰器可以在启动时执行一次，也可以自己指定启动时机，但请注意这是一个永不停止的线程不安全，使用与停止时还请注意。
```py
import mods

bot_self_id= '1234567890'
my_channel_id = '1234567890'


@mods.on.bot_start_up
@mods.timer_do('23:00')
def clock1():
    event = mods.Event()
    event.platform = 'red'
    event.self_id = bot_self_id
    event.message_create(channel_id=my_channel_id, content='你今天贴瓷砖了吗！')

    
@mods.on.bot_start_up
@mods.interval_do(8*60*60,do_now=False)
def back_up():
    # 备份数据库
    import os
    os.system('cp db.sqlite3 db.sqlite3.bak')
 ```

> 利用来自 `mods` 的 `config` 与 `assets` 实现资源配置

need 用于检查配置是否存在，不存在则写入默认值。(需要重启重载)
```py
import mods
mods.config.need('my_img_path', mods.assets("my_img.png"))
img = mods.assets(mods.config.get_key('my_img_path'))
```

> 利用来自 `core` 的 `log` 打印日志
```py   
import mods
mods.log.info('info')
mods.log.warning('warning')
mods.log.error('error')
mods.log.debug('debug')
mods.log.success('success')
```




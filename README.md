

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
## 📖 介绍


`Tomorin` 是一个基于 [Satori协议](https://satori.js.org/zh-CN/) 的迷你家用聊天机器人框架。
使用装饰器标记函数，使得在收到各类信息时或指定状态时，对应函数被调用。

## 💫 运行

```shell
pip install httpx websocket-client
```

```shell
python -m core
```

~~可以使用 `hupper` 来实现热重启。~~


首次运行时会生成一个 `config.json` 文件，你需要主动关闭应用，在其中填写你的合适的配置后重启以加载新的配置。

## 📚 异步与多线程支持

`Tomorin` 同时支持异步与多线程。
> 请不要混用或尝试数据共享，这可能会导致不可预知的错误。

`Tomorin` 的 `WebSocket` 连接在收到消息推送时候分别通过 `asyncio.create_task` 与 `threading.Thread` 来同时构建两个不同的 `Event` / `EventAsync` 对象，分别不阻塞地调用注册的函数。

`asyncio.create_task` 位于主线程，可以放心使用诸如 `Alconna` 等使用了 `contextvars` 的库而不会出现线程错误问题。

## 👋 插件编写前的准备

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
这个时候包 `foo` 同样是一个合法的插件，插件内容可以在 `__init__.py` 文件中编写。

但 `Tomorin` 的插件也只起到被导入的作用，而要做到在某种情况下调用函数，请看 `on` 装饰器。
## 📦 插件编写

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

need 用于检查配置是否存在，不存在则写入默认值。(需要重启重载)
```py
from core.interfaces import config
config.need('my_img_path', "plugs/my_plug/my_img.png")
img_path = config.get_key('my_img_path')
```

- 利用来自 `core` 的 `log` 打印日志，`c` 为颜色类，可以使用 `c.bright_green` 等属性来设置颜色。
```py   
from core.interfaces import log, c
log.info('info')
log.warning('warning')
log.error('error')
log.debug('debug')
log.success('success')


log.info(f'{c.bright_green}这是绿色的字{c.reset}')
log.info(f'{c.bg.red}{c.bright_white}这是红色背景的字{c.reset}')
log.info(f'{c.style.underline}这是下划线{c.reset}')
```

## 📄 关于
本模版出发点是学习与探索设计方法，让简单的功能实现可以高速产出。   

## 🧩 `mods` 扩展


> `mods` 扩展并不是框架行为，而是一个方便使用的依赖包。
> 如果你不喜欢这种形式，可以删除 `mods` 。


- 使用 match_command 扩展实现一个 `echo` 命令
```py
import mods

# mods 继承了 core 的 interface，所以可以直接使用
@mods.on.message_created
def echo_(event: mods.Event):
    if res := mods.match_command(event, 'echo', limit_admin=True, allow_gap_less=True):
        res.send(res.text)
```

- 使用来自 mods` 的 `h` 在入群时发送一张图片
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

- 使用来自 `mods` 的 定时器 与 间隔器 实现常规定时任务。   
- 
> 请注意，定时器与间隔器的时间单位为秒，且定时器会在启动时立即执行一次，可以通过 `do_now` 参数控制是否立即执行。   
通过 `@mods.on.bot_start_up` 装饰器可以在启动时执行一次，也可以自己指定启动时机，但请注意这是一个永不停止的线程不安全，使用与停止时还请注意。
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
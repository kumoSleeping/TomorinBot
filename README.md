


# md文档版本落后，请以实际为准


<h1 align="center"> Tomorin BOT </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v0.2.0</div>
<div align="center">  人間になりたいうた...
</div>


***

## 概述

如你所见，Tomorin Bot是一个基于Satori协议的聊天机器人后端框架，你可以方便地在框架基础上实现各种功能。

注意，Tomorin Bot**不是**用于与聊天平台直接交互的前端。

------

## 快速使用

### 填写配置

启动Tomorin Bot前，请先填写 `config.yml`：

```yaml
server:
  #  默认 0.0.0.0
  ip: '0.0.0.0'
  #  默认 5500
  port: '5140'
  # 没有就随便填
  token: ''
  # 心跳间隔 < 10 ，单位秒
  HeartbeatInterval: 5
user:
  # 管理员用户，不论平台（暂时没支持）
  administrator: []
```

如果你不知道如何填写 `ip` 和 `port`，请参考你使用的机器人前端文档。

### 启动Tomorin Bot

填写`config.yml`后，你可以通过下面的命令运行Tomorin Bot：

```bash
python server.py
# python3 server.py
```

如果你的操作正确，Tomorin Bot便已经可以和前端进行通信了。

------

## 实现功能

### 创建你的第一个组件

打开`./plugin_package/component.py`，机器人所有的**组件**都位于这个文件。   
你会发现很多样板函数，例如下方的`test1`。  


```python
@component
def test1(session):
    if session.message.content == '测试文字':
        send(f'测试成功！', session)
```
不难看出，当机器人会话内信息文字为**测试文字**，机器人就会回复**测试成功！**。

### 使用组件实现更多功能

**组件**(component)是在 `component.py` 中定义的一组函数，它们被修饰器 `@component` 标识，接受一个 `Session` 参数，并在函数体中处理对应的消息。
组件适用于~~开发者偷懒不想使用插件~~快速实现简单的功能。

让我们参考下面的实例：

```python
# component.py
# ...省略前面的import语句

@component
def test1(session):
    # 根据消息内容处理消息
    if session.message.content == '测试文字':
        # 使用session对象的send函数响应消息
        # 这是以纯文字消息进行回复的例子
        # 关于session对象后面会有更详细的介绍
        session.send('测试成功！')


@component
def test2(session):
    if session.message.content == '测试音频':
        # 这是以音频消息进行回复的例子
        # 在这里我们使用h中的函数来构建audio消息元素
        # 同样，我们会在后面详细介绍消息元素
        session.send(f'{h.audio("https://bestdori.com/assets/jp/sound/bgm542_rip/bgm542.mp3")}')


@component
def test3(session):
    if session.message.content == '测试混合元素':
        # 这是以多个元素构建消息进行回复的例子
        # 我们创建一个PIL图片对象来进行测试
        # h中也提供了直接以PIL对象构建图片消息元素的函数
        image = Image.new('RGB', (50, 50), color='red')
        # 下面的消息中混合了“回复” “@” “文字” “图片”四种元素
        session.send(f'{h.quote(session.message.id)} {h.at(session.user.id)} 爱城华恋色图：{h.image(image)}')


@component
def test4(session):
    # 可以通过截取消息内容来实现类似指令的功能
    if session.message.content.startswith('发送到群组'):
        # 取“发动到群组”后面指定的群号
        forward_guild_id: str = session.message.content[5:].strip()
        # 在这里我们使用bot.send函数以向频道（群聊）发送消息
        # bot相关的函数也会在后面介绍
        rpl = bot.send(f'这是一条来自 {session.guild.name} 的消息', session.platform, forward_guild_id, session.self_id)
        # 通过解析返回值确认消息是否成功发送
        if not rpl:
            session.send(f"发送失败")
        else:
            session.send('发送成功')
```

在上面的实例中，我们定义了四个组件来处理消息，你可以参考注释来理解它们。

### 内置组件 / 服务

你会发现在`component.py`中内置了一个`_soyorin`组件。

这是一个平台信息屏蔽组件。

当储存的信息关系和本次session的信息一致时，`_soyorin`会判断此消息不容许发出。

### 创建插件

如果你需要实现大型的功能，请考虑使用插件，这更有利于你持久化地维护你的功能。

插件有自己的文件夹，所以不用合租，~~有的舍友就是很让人讨厌~~。   

让我们在 `./plugins` 下新建一个英文名文件夹，我们就给这个文件夹取名为 `foo`。此时，`foo` 就是这个插件的名字。  

插件以 `index.py` 文件中的 `src` 函数作为入口点。

例如，我们现在在 `foo` 文件夹中新建 `index.py`，然后实现 `src` 函数：

```python
# index.py
import time

# 关于core中的内容也会在后面介绍
from core.Rana import h

# 插件入口点
def src(session):
    if session.message.content == 'foo':
        # 使用xml元素提及用户，正常推荐使用 h.at(session.user.id)
        msg_id = session.send(f'<at id="{session.user.id}"/> bar')

        time.sleep(3)
        # 尝试撤回消息（如果平台支持这个API）
        rpl = session.call_api(method='message.delete', data={"message_id": msg_id, "channel_id": session.channel.id})
        # print(rpl)
```

当收到的消息是**foo**时，BOT将会发送一条消息：**@用户 bar**，等待三秒后，尝试撤回消息。  

你可能注意到我们没有用到 `h` 来包装消息，而是直接使用xml代码来写消息元素。

Tomorin Bot支持用这种方式来表示消息元素，但非必要的情况下我们仍推荐你使用 `h` 中的函数。


***
## 深入理解

### 基础跨平台概念

如果你想使用Tomorin Bot进行跨平台bot开发，你必须了解下面的概念：

**平台 (Platform)** 是指聊天平台，比如 Discord、Telegram 等。同一平台内的用户间具有相互发送消息的能力，而不同平台的用户间则没有。对于 Rocket Chat 这一类可自建的聊天平台而言，每个独立的自建服务器都视为不同的平台。

**机器人 (Bot)** 是指由 Koishi 操控的平台用户。这里的用户可以是真实用户，也可以是部分平台专门提供的机器人用户。其他用户通过与机器人进行交互来体验 Koishi 的各项功能。

**适配器 (Adapter)** 是指实现了平台协议，能够让机器人接入平台的插件。通常来说一个适配器实例对应了一个机器人用户，同时启用多个适配器就实现了多个机器人的同时接入。

**消息 (Message)** 是字面意义上的消息。通常是文本或富文本格式的，有时也会包含图片、语音等媒体资源。在 Koishi 中，消息通过消息元素进行统一编码。

**频道 (Channel)** 是消息的集合。一个频道包含了具备时间、逻辑顺序的一系列消息。频道又分为私聊频道和群聊频道，其中私聊频道有且仅有两人参与，而群聊频道可以有任意多人参与。

**群组 (Guild)** 是平台用户的集合。一个群组通常会同时包含一组用户和频道，并通过权限机制让其中的部分用户进行管理。在部分平台中，群组和群聊频道的概念恰好是重合的 (例如 QQ)：一个群组内有且仅有一个群聊频道。私聊频道不属于任何群组。

以上内容来自[Koishi开发文档](https://koishi.chat/zh-CN/guide/adapter/)。   

~~是的，Tomorin Bot还没有自己的开发文档。~~

### Tomorin Bot Core概述

如果你想使用Tomorin Bot框架构建大型项目，我们建议你了解Tomorin Bot框架的核心内容。

Tomorin Bot的核心内容在 `core` 文件夹下，其中文件的命名来自MyGO!!!!!。

- Ano.py   
  通过ws与前端进行通讯，并在收到数据尝试调用 `main()` 函数。   
  由于异步实现遇到了一些困难，Tomorin Bot现在使用 AnonTokyo.py进行同步ws通信。
- **AnonTokyo.py**   
  实现与Bot前端的web socket通信，包括登陆、心跳、鉴权、消息处理等。   
  接收到消息时，将消息数据转交 `Tomorin.py` 中的 `main()` 函数处理。   
- **Tomorin.py**
  在 `main()` 函数中，Tomorin Bot会解析前端发送的数据，通过**Rana**构建Session对象以供后续处理。   
  同时，也会调用**Soyorin**中的BanManager进行消息审核。   
  插件、组件加载也在这里进行。   
- **Rana.py**   
  主要负责前端以Satori协议传回数据的解析，并抽象了基础的消息对象。   
  同时提供了快速构建消息元素的 `h` 相关函数。   
- **Soyorin.py**   
  进行消息审核、插件管理、日志显示，并实现了一套黑白名单API。   
- **Rikki.py**   
  以Satori协议向前端发送POST请求，实现各种API上报，如消息发送等。   

### Session对象

如前所述，Session对象是Rana构建的基础消息抽象，提供了消息的基本信息。

**属性**:  

- `id` (str): 会话ID。
- `type` (str): 会话类型。
- `platform` (str): 会话所在平台。
- `self_id` (str): 机器人自身的ID。
- `timestamp` (str): 消息时间戳。
- `user` (User): 包含用户信息的实例。
  - `id` (str): 用户ID。
  - `name` (str): 用户名。
  - `avatar` (str): 用户头像。
- `channel` (Channel): 包含频道信息的实例。
  - `type` (str): 频道类型。
  - `id` (str): ID。
  - `name` (str): 频道名。
- `guild` (Guild): 包含群组信息的实例。
  - `id` (str): 群组ID。
  - `name` (str): 群组名。
  - `avatar` (str): 群组头像。
- `member` (dict): 成员信息字典。
  - `name` (str): 成员名。
- `message` (Message): 包含消息信息的实例。
  - `id` (str): 消息ID。
  - `content` (str): 消息内容。
  - `elements` (str): 消息元素。

**函数:**

- `send()`: 快速响应消息。
- `call_api()`: 直接调用Satori标准API，通常用于跨平台开发或未抽象的功能。

在前面实现功能的例子中我们已经多次用到了Session对象，这里就不再举例。

### 消息元素

在bot开发中，我们往往不止需要处理纯文字消息，还会遇到图片、音频等内容。

我们使用xml消息元素来支持这些富元素消息。Satori支持的xml元素具体可以参考 [Koishi元素](https://koishi.chat/zh-CN/api/message/elements.html)。   

直接在消息中写xml元素，即可发送富元素消息。这也是jsx很经典的用法。

例子如下：

```python
# 这条消息含有 quote 和 at 元素
msg = f'<quote id="{session.message.id}"/> <at id="{session.user.id}"/>你好'
```

当然，我们也在实现功能一节的举例已经使用到了消息元素，你可能还记得使用 `h` 系列函数来快速构建消息元素的方法。

我们认为在python代码中使用xml有一种在祥子面前演奏春日影的美。

因此，Rana的 `h` 对象包含了一组辅助方法，用于生成标准消息元素的xml字符串。

~~现在有一种Tomorin在Rana的鼓动下在祥子面前演奏春日影的美了。~~

**普通方法列表**

- `at(user_id)`: 生成@某用户。
- `sharp(channel_id)`: 生成#某频道消息内容。
- `quote(message_id)`: 生成引用。
- `text(content)`: 生成文本（多数情况无需使用此API生成）。

**类型自动判断方法列表**

- `image(param)`: 生成图片（通过URL / 缓冲区buffer / Pillow Image对象）。
- `audio(param)`: 生成音频（通过URL / 缓冲区buffer）。
- `video(param)`: 生成视频（通过URL / 缓冲区buffer）。
- `file(param)`: 生成文件（通过URL / 缓冲区buffer）。


例子如下：

```python
# 新建PIL对象
image = Image.new('RGB', (50, 50), color='red')
# 回复元素 提及元素 图片元素
msg = f'{h.quote(session.message.id)} {h.at(session.user.id)} 爱城华恋色图：{h.image(image)}'

```

### 发送消息 / 调用API

Rikki实现了`Rikki.send_request`来请求Satori标准API。

在此基础上，我们可以通过 `bot` 和 `session` 对象发送消息与请求。   

#### bot方法

- `bot.send()`
- `bot.call_api()`

bot方法需要传入的参数较多，一般用于跨群聊 / 平台插件。 
```python
rpl = bot.send(f'这是一条来自 {session.guild.name} 的消息', session.platform, forward_guild_id, session.self_id)
```


#### session方法
- `session.send()`
- `session.call_api()`

session方法会为必要信息尽可能的自动填入本次会话的信息。
例如一问一答的时候，使用`session.send()`只需要传入回答的消息，即可发送到本此会话所发生的地方。


#### 调用 API
使用`call_api`调用。

[Satori文档-api](https://satori.js.org/zh-CN/protocol/api.html)   
[Satori文档-内部接口](https://satori.js.org/zh-CN/protocol/internal.html)
如果你使用Koishi的Server插件作为万用适配器，请查看[Koishi官方插件](https://koishi.chat/zh-CN/plugins/)指南了解各个平台内部API接口。   






## More

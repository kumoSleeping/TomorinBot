


# md文档版本落后，请以实际为准


<h1 align="center"> Tomorin BOT </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v0.2.0</div>
<div align="center">  人間になりたいうた...
</div>


***



## 快速开始：

填写`config.yml`后，运行：

```bash
python server.py
# python3 server.py
```

## 使用组件快速创建第一个功能
打开`./plugin_package/component.py`，机器人所有的**组件**都位于这个文件。   
你会发现很多样板函数，例如下方的`test1`。  


```python
@component
def test1(session):
    if session.message.content == '测试文字':
        send(f'测试成功！', session)
```
不难看出，当机器人会话内信息文字为**测试文字**，机器人就会回复**测试成功！**。

你可以适当修改一下文字部分，修改完保存重启`server.py`后，第一个功能就会被搭载完毕。




***
## 发送消息 / 调用API
Rikki提供了`Rikki.send_request`请求Satori标准API。   
在此基础上，目前有两个方法发送消息与请求。   

### bot方法

- `bot.send()`
- `bot.call_api()`

bot方法需要传入的参数较多，一般用于跨群聊 / 平台插件。   
eg：
```python
rpl = bot.send(f'这是一条来自 {session.guild.name} 的消息', session.platform, forward_guild_id, session.self_id)
```


### session方法
- `session.send()`
- `session.call_api()`

session方法会为必要信息尽可能的自动填入本次会话的信息。   
例如一问一答的时候，使用`session.send()`只需要传入回答的消息，即可发送到本此会话所发生的地方。


### 调用 API
使用`call_api`调用。

[Satori文档-api](https://satori.js.org/zh-CN/protocol/api.html)   
[Satori文档-内部接口](https://satori.js.org/zh-CN/protocol/internal.html)
如果你使用Koishi的Server插件作为万用适配器，请查看[Koishi官方插件](https://koishi.chat/zh-CN/plugins/)指南了解各个平台内部API接口。   

## 消息元素

### xml元素发送

Satori支持的xml元素具体可以参考 [Koishi元素](https://koishi.chat/zh-CN/api/message/elements.html)。   

也就是说，直接在消息中加入元素，即可发送富元素消息。这也是jsx很经典的用法。

eg：
```python
# 这条消息含有 quote 和 at 元素
msg = f'<quote id="{session.message.id}"/> <at id="{session.user.id}"/>你好'
```

### 快捷调用
说实话我一直觉得在py里使用xml有一种牛的美。   
因此，Rana的 `h` 方法包含了一组辅助方法，用于生成标准元素字符串。   

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


eg:
```python
# 新建PIL对象
image = Image.new('RGB', (50, 50), color='red')
# 回复元素 提及元素 图片元素
msg = f'{h.quote(session.message.id)} {h.at(session.user.id)} 爱城华恋色图：{h.image(image)}'

```


## 接收到的信息

### 核心概念
在我们开始之前，先来了解一些与跨平台相关的核心概念。

**平台 (Platform)** 是指聊天平台，比如 Discord、Telegram 等。同一平台内的用户间具有相互发送消息的能力，而不同平台的用户间则没有。对于 Rocket Chat 这一类可自建的聊天平台而言，每个独立的自建服务器都视为不同的平台。

**机器人 (Bot)** 是指由 Koishi 操控的平台用户。这里的用户可以是真实用户，也可以是部分平台专门提供的机器人用户。其他用户通过与机器人进行交互来体验 Koishi 的各项功能。

**适配器 (Adapter)** 是指实现了平台协议，能够让机器人接入平台的插件。通常来说一个适配器实例对应了一个机器人用户，同时启用多个适配器就实现了多个机器人的同时接入。

**消息 (Message)** 是字面意义上的消息。通常是文本或富文本格式的，有时也会包含图片、语音等媒体资源。在 Koishi 中，消息通过消息元素进行统一编码。

**频道 (Channel)** 是消息的集合。一个频道包含了具备时间、逻辑顺序的一系列消息。频道又分为私聊频道和群聊频道，其中私聊频道有且仅有两人参与，而群聊频道可以有任意多人参与。

**群组 (Guild)** 是平台用户的集合。一个群组通常会同时包含一组用户和频道，并通过权限机制让其中的部分用户进行管理。在部分平台中，群组和群聊频道的概念恰好是重合的 (例如 QQ)：一个群组内有且仅有一个群聊频道。私聊频道不属于任何群组。

以上内容来自[Koishi开发文档](https://koishi.chat/zh-CN/guide/adapter/)。   

### Session类


Session 类包装了接收到的消息的基础信息。   
构造函数，创建一个 Session 实例 session。   

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


eg:
```python
# 消息内容
mc = session.message.content
# 用户ID
userID = session.user.id
```



## 创建更多功能

在TomorinBOT项目模版中，创建功能可以使用**插件**或**组件**的形式。   
可以按照喜好自由选择。   

### 一个新的插件（plugin） 
首先，您需要在`./plugin_package`，新建一个英文名文件夹，我们就给这个文件夹取名为foo。此时，foo就是这个插件的名字。  
`./foo`文件夹内需要一个`index.py`作为入口文件，文件内需要一个`src`函数作为主函数。   
下面是一个标准例子。   
```python
# index.py
import time

from core.Rana import h


def src(session):
    if session.message.content == 'foo':
        # 使用xml元素提及用户，正常推荐使用 h.at(session.user.id)
        msg_id = session.send(f'<at id="{session.user.id}"/> bar')

        time.sleep(3)
        # 尝试撤回消息（前提是平台支持这个API）
        rpl = session.call_api(method='message.delete', data={"message_id": msg_id, "channel_id": session.channel.id})
        # print(rpl)
```
不难看出，当本次消息的"消息内容"和"foo"一致时，BOT将会发送一条消息：提及用户，消息内容是"bar"。  
然后等待三秒。   
尝试撤回消息。  

本例子中，没有需要用到`Rana`的`h`包装消息，而是直接使用xml元素。   
使用`session.send`发送消息。 

### 组件（component）
`component.py`是一个组件文件。   
所有的组件都作为`component.py`的函数，使用`@component`修饰器以标识。
使用组件更多是因为开发者比较懒，懒得新建一个文件夹，就把功能都堆在一起了。   

我在组件里给了如下生产案例：
```python
# component.py
# ...省略前面

@component
def test1(session):
    if session.message.content == '测试文字':
        session.send('测试成功！')


@component
def test2(session):
    if session.message.content == '测试音频':
        session.send(f'{h.audio("https://bestdori.com/assets/jp/sound/bgm542_rip/bgm542.mp3")}')


@component
def test3(session):
    if session.message.content == '测试混合元素':
        image = Image.new('RGB', (50, 50), color='red')
        # h.image(image) 可以直接通过传 PIL 对象发送图片
        session.send(f'{h.quote(session.message.id)} {h.at(session.user.id)} 爱城华恋色图：{h.image(image)}')


@component
def test4(session):
    if session.message.content.startswith('发送到群组'):
        forward_guild_id: str = session.message.content[5:].strip()
        rpl = bot.send(f'这是一条来自 {session.guild.name} 的消息', session.platform, forward_guild_id, session.self_id)
        if not rpl:
            session.send(f"发送失败")
        else:
            session.send('发送成功')
```
您可以尝试理解上面的例子，如果理解有问题可以咨询一些AI工具或者是您的亲朋好友的帮助。

     




### 插件 / 组件 数据
进入 `./plugin_package` 文件夹，你会发现有一个 `./_plugin_data` 文件夹，按照规范请组件数据放在这里，不要到处乱拉。当然你不放这也行。      
插件有自己的文件夹所以不用合租，有的舍友就是很让人讨厌。   


## 内置插件 - 服务

你会发现在`component.py`中内置了一个`_soyorin`组件。   
这是一个平台信息屏蔽组件。   
当储存的信息关系和本次session的信息一致时，`_soyorin`会判断此消息不容许发出。





## ./core介绍：
现在你需要了解一下这个python项目模版的内部，以便于更好的使用与扩展。   

本项目模版的`./core`部分命名来自MyGO!!!!!中的成员。

Ano.py   
进行ws连接。   
收到数据尝试启动 main() 函数。   

Tmorin.py   
提供 main()函数，先解析数据到session，审核消息，然后启动每个组件和插件包。

Rana.py   
提供 Rana.process_satori_message() 函数解析数据到session。   
提供发送消息时包装元素的 h() 函数，返回xml格式信息。  

Soyorin.py   
读取配置文件，获取全局变量。      
提供BanManager消息审核，Soyorin.show_session_log日志显示，正反向转译字符函数。   


Rikki.py   
基于 Rikki.send_request() 函数，提供 send(), h_send(), in_api(), h_in_api() 函数用于发送信息 / 内部请求。


## More




<h1 align="center"> Tomorin BOT </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v0.2.0</div>
<div align="center">  人間になりたいうた...
</div>


***


## 成员介绍：

Ano.py   
程序启动入口    
对「satori」协议进行连接 / 数据包获取 / 心跳保活   
为每个会话启动 main(data)   

Tmorin.py   
main 处理所有插件   
核心处理调度 data 和 发送

Rana.py   
对「satori」协议进行基础消息抽象 / 日志显示   
提供平台包装元素的 API   

Soyorin.py   
消息审核 / 插件管理 / 黑白名单 API   
与 ./plugin 界限模糊，类似服务组件 API   

Rikki.py   
处理「satori」协议的信息发送 / API上报
```markdown
小知识：
1.程序开始于Ano.py。
2.Rikki.py 只会在 Tmorin.py 被调用。
3.Soyorin.py Tmorin.py 可能永远都不会随着适配器而改变。
4.Tmorin.py 永远是 Bot 的核心。
```


## 快速开始：

```bash
python server.py
# python3 server.py
```

### server.py

启动！

***
## 发送元素消息

Satori支持的xml元素具体可以参考 [Koishi元素](https://koishi.chat/zh-CN/api/message/elements.html)   
Rana的 `h` 类包含了一组辅助方法，用于生成特定格式的标准元素消息内容。   

**方法列表**

- `text(content)`: 生成文本消息内容。
- `at(user_id)`: 生成@某用户消息内容。
- `sharp(channel_id)`: 生成#某频道消息内容。
- `quote(message_id)`: 生成引用消息内容。
- `image_url(url)`: 生成图片消息内容（通过URL）。
- `audio_url(url)`: 生成音频消息内容（通过URL）。
- `video_url(url)`: 生成视频消息内容（通过URL）。
- `file_url(url)`: 生成文件消息内容（通过URL）。
- `image_buffer(buffer, mime_type='image/png')`: 生成图片消息内容（通过缓冲区）。
- `image_pil(image, mime_type='image/png')`: 生成图片消息内容（通过Pillow Image对象）。
- `audio_buffer(buffer, mime_type='audio/mpeg')`: 生成音频消息内容（通过缓冲区）。
- `video_buffer(buffer, mime_type='video/mp4')`: 生成视频消息内容（通过缓冲区）。
- `file_buffer(buffer, mime_type='application/octet-stream')`: 生成文件消息内容（通过缓冲区）。

eg:
```python
# 新建PIL对象
image = Image.new('RGB', (50, 50), color='red')
# 回复元素 提及元素 图片元素
msg = f'{h.quote(session.message.id)} {h.at(session.user.id)} 爱城华恋色图：{h.image_pil(image)}'
# 也可以使用xml表示
# msg = f'<quote id="{session.message.id}"/> <at id="{session.user.id}"/> '

```


## 接收到的信息


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
- `channel` (Channel): 包含渠道信息的实例。
  - `type` (str): 渠道类型。
  - `id` (str): 渠道ID。
  - `name` (str): 渠道名。
- `guild` (Guild): 包含服务器信息的实例。
  - `id` (str): 服务器ID。
  - `name` (str): 服务器名。
  - `avatar` (str): 服务器头像。
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
userID = session.uer.id
```



## 创建第一个功能

在TomorinBOT中，创建功能可以使用**插件**或**组件**的形式。   
可以按照喜好自由选择。   

### 一个新的组件（component）
`component.py`是一个组件文件。   
所有的组件都作为`component.py`的函数，使用`@component`修饰器以标识。

```python
# component.py
# ...省略前面
@component
def hello(session):
    if session.message.content == '测试音频':
        send(f'{h.audio_url("https://bestdori.com/assets/jp/sound/bgm542_rip/bgm542.mp3")}', session)
```
不难看出，当本次消息的"消息内容"和"测试音频"一致时，BOT将会发送一条音频消息，从网络url获取。

### 一个新的插件（plugin）
`./foo` 文件夹是一个插件包示例。   
文件夹内的`index.py`作为入口文件。
```python
# index.py
from core.Rana import h
from core.Rikki import send


def src(session):
    if session.message.content == 'foo':
        send(f'{h.quote(session.message.id)} {h.at(session.user.id)} bar', session)
```
不难看出，当本次消息的"消息内容"和"foo"一致时，BOT将会发送一条消息，回复用户本条消息，提及用户，消息内容是"bar"。

本例子中，需要用到`Rana`的`h`解析消息，和`Rikki`的`send`发送消息。      




### 插件 / 组件 数据
进入 `./plugin_package` 文件夹，你会发现有一个 `./_plugin_data` 文件夹，按照规范请把插件 / 组件数据放在这里。   
当然你不放这也行。   


## 内置插件 - 服务

你会发现在`component.py`中内置了一个`_soyorin`组件。   
这是一个平台信息屏蔽组件。   
当储存的信息关系和本次session的信息一致时，`_soyorin`会判断此消息不容许发出。




## core介绍

### ./core

首先，被启动的是 `Ano.py` 用于收获来自外界的 **消息** 。

`Ano.py` 收到 **消息** 后，调用 `Tomorin.py` 并传入 **消息** 。

`Tomorin.py` 会调用 `Soyo.py` 的第一部分对 **消息** 解析抽象、审查合格性。

`Soyo.py` 通过后， **消息** 会继续回到 `Tomorin.py` 

`Tomorin.py` 此时获得了 **抽象后的消息** ，此时消息会被 **正式处理** 为 **被发送的消息**。

**正式处理**后，`Tomorin.py` 会调用`Soyo.py` 的第二部分对 **被发送的消息** 进行 打包、审查合格性。

`Soyo.py` 通过后，`Rikki.py` 会被 `Tomorin.py` 作为 **消息发送器** 调用，直接尝试发送 **被发送的消息** 。




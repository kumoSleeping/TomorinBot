


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



## 创建更多功能

在TomorinBOT项目模版中，创建功能可以使用**插件**或**组件**的形式。   
可以按照喜好自由选择。   

### 一个新的插件（plugin） 
首先，您需要在`./plugin_package`，新建一个英文名文件夹，我们就给这个文件夹取名为foo。此时，foo就是这个插件的名字。  
`./foo`文件夹内需要一个`index.py`作为入口文件，文件内需要一个src函数作为主函数。   
下面是一个标准例子。   
```python
# index.py
import time

from core.Rana import h
from core.Rikki import send


def src(session):
    if session.message.content == 'foo':
        send(f'思考...', session)
        time.sleep(3)
        send(f'{h.quote(session.message.id)} {h.at(session.user.id)} bar', session)
```
不难看出，当本次消息的"消息内容"和"foo"一致时，BOT将会发送一条消息：消息内容是"思考..."。   
然后等待三秒。   
再次发送一条消息：回复用户本条消息，提及用户，消息内容是"bar"。  

本例子中，需要用到`Rana`的`h`解析消息，和`Rikki`的`send`发送消息。 

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
        send(f'测试成功！', session)


@component
def test2(session):
    if session.message.content == '测试音频':
        send(f'{h.audio_url("https://bestdori.com/assets/jp/sound/bgm542_rip/bgm542.mp3")}', session)


@component
def test3(session):
    if session.message.content == '测试混合元素':
        image = Image.new('RGB', (50, 50), color='red')
        send(f'{h.quote(session.message.id)} {h.at(session.user.id)} 爱城华恋色图：{h.image_pil(image)}', session)


@component
def test4(session):
    if session.message.content.startswith('发送到群组'):
        forward_guild_id: str = session.message.content[5:].strip()
        rpl = h_send(f'这是一条来自 {session.guild.name} 的消息', session.platform, forward_guild_id, session.self_id)
        if not rpl:
            send(f"发送失败", session)
        else:
            send('发送成功', session)
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
提供 main()函数，先解析数据到session，然后审核消息，然后启动每个组件和插件包。

Rana.py   
提供 Rana.process_satori_message() 函数解析数据到session。   
提供发送消息时包装元素的 h() 函数，返回xml格式信息。  

Soyorin.py   
读取配置文件，获取全局变量。      
提供BanManager消息审核，Soyorin.show_session_log日志显示，正反向转译字符函数。   


Rikki.py   
基于 Rikki.send_request() 函数，提供 send(), h_send(), in_api(), h_in_api() 函数用于发送信息 / 内部请求。


## More

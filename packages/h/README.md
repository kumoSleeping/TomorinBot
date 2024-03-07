
# h 
包装元素

## 导入

```python
from plugins.h import h
```

## 概述

在bot开发中，我们往往不止需要处理纯文字消息，还会遇到图片、音频等内容。

我们使用xml消息元素来支持这些富元素消息。Satori支持的xml元素具体可以参考 [Koishi元素](https://koishi.chat/zh-CN/api/message/elements.html)。   

直接在消息中写xml元素，即可发送富元素消息。这也是jsx很经典的用法。

例子如下：

```python
# 这条消息含有 quote 和 at 元素
msg = f'<quote id="{event.message.id}"/> <at id="{event.user.id}"/>你好'
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
from plugins.h import h
# 新建PIL对象
image = Image.new('RGB', (50, 50), color='red')
# 回复元素 提及元素 图片元素
msg = f'{h.quote(session.message.id)} {h.at(session.user.id)} 爱城华恋色图：{h.image(image)}'

```
```python
from plugins.h import h

h.image('https://koishi.chat/logo.png')
h.quote('1938410823901')
h.at('1233534324')
```

*end.*


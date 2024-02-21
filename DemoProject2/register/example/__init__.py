from core import on, Event
from modules import match_command, h


@on.message_created
def m_w(event: Event):
    if res := match_command(event, ['miao', '喵'], arg_less=True):
        if event.message.content == 'miao':
            event.message_create('woof!')
        elif event.message.content == '喵':
            event.message_create('汪！')


@on.message_created
def test_pic(event: Event):
    if res := match_command(event, 'test_pic', arg_less=True):
        # 打开图片
        with open('register/example/eg.jpg', 'rb') as f:
            img = f.read()
        res.send(h.image(img))




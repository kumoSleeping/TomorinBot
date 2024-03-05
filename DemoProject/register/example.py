from core import on, Event
from core import match_command, h


@on.message_created
def m_w(event: Event):
    if res := match_command(event, ['miao', '喵'], arg_less=True):
        if event.message.content == 'miao':
            event.message_create('woof!')
        elif event.message.content == '喵':
            event.message_create('汪！')




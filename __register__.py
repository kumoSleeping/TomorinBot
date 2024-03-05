# from register.example import *


# 这里是插件的注册，也就是导入 @on.xxx 的函数的声明


from core import on, Event, h


@on.message_created
def miao_woof(event: Event):
    print("New Msg: " + event.message.content)
    if event.message.content.startswith("miao"):
        event.message_create("woof" + h.at(event.user.id))


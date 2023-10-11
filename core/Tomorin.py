import json
import re
from .Rana import process_satori_message
from .Rikki import send

'''
Tmorin.py
处理所有插件
核心处理调度 data 和 发送
'''

plugin_configurations = []


def plugin(func):
    plugin_configurations.append(func)


def Main(data):
    session = process_satori_message(data)
    for plugin in plugin_configurations:
        plugin(session)


@plugin
def hello(session):
    if session.message.content == '你好':
        send('你好喵（', session)

@plugin
def photo_(session):
    if session.message.content == '11':
        send(f'<at id="{session.user.id}"/> 喵喵', session)



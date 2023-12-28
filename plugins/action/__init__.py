from core import on, Event
from typing import Optional
from typing import Union, Callable
import inspect


from plugins.message_content_tools import plaintext_if_prefix, remove_all_xml

# 启用qq被动功能
from plugins.action.qq_passive import qq_passive__
# 启用help功能
from plugins.action.help import help__


class Action:
    def __init__(self, event: Event):
        self.event: Event = event
        self.is_did: bool = False  # 是否已经执行过

        pure_msg = self.event.message.content
        pure_msg = remove_all_xml(pure_msg)
        pure_msg = plaintext_if_prefix(pure_msg).strip()
        if pure_msg == '':
            self.is_did = True

        self.pure_msg = pure_msg

        self.args: list = []  # 参数
        self.text: str = ''  # 文本
        self.description: str = ''  # 描述

        self.seq: int = 0

    def cutshort(self, cutshort: list, function: Callable):
        for item in cutshort:
            if item == self.pure_msg:
                self.args = []
                self.text = cutshort
                self._call(function)
                return self
        return self

    def command(self, command: list, function: Callable):
        for item in command:
            cmd = self.pure_msg.split()[0] if len(self.pure_msg.split()) > 0 else ''
            if item.startswith(cmd + ' '):
                self.args = self.pure_msg.split()[1:]
                self.text = self.pure_msg.replace(cmd + ' ', '', 1)
                self._call(function)
                return self
            elif item == cmd:
                self.args = self.pure_msg.split()[1:]
                self.text = self.pure_msg.replace(cmd + ' ', '', 1)
                self._call(function)
                return self
        return self

    def do(self, function: Callable):
        self.args =[]
        self.text = self.pure_msg
        self._call(function)
        return self

    # 实现一个装饰器
    def send(self, message_content: str):
        try:
            print('[action] send -> ' + self.event.platform)
            message_content = qq_passive__(self, message_content)
        except:
            pass
        return self.event.message_create(channel_id=self.event.channel.id, content=message_content)

    def _call(self, function: Callable):
        if self.args:
            try:
                 help__(self)
            except Exception as e:
                print(e)
        if self.is_did:
            return self

        self.is_did = True
        function(self)
        return self



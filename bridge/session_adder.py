from enum import IntEnum
from typing import Union, Optional
import re

from core.config import config
from core.session_maker import Session
from core.api import Api


class Command:
    def __init__(self, command_name, args, text):
        self.command_name: str = command_name
        self.args: list = args
        self.text: str = text


class SessionExtension(Session):
    def __init__(self, body: dict):
        super().__init__(body)
        self.command: Optional[Command] = None

    def send(self, message_content: str):
        # 使用实例属性时，直接通过 self 访问
        print(f'[ send -> {self.platform}: {self.channel.name} ] ')
        if self.platform == 'qq' and '<qq:passive id=' not in message_content:
            message_content = message_content + f'<qq:passive id="{self.message.id}"/>'
        return Api.message_create(self, channel_id=self.channel.id or self.guild.id, content=message_content)






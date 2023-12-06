from enum import IntEnum
from typing import Union, Optional
import re

from api import Api

'''
Rana.py
对「satori」协议进行基础消息抽象 / 日志显示
提供平台包装元素的 API
'''


class ChannelType(IntEnum):
    TEXT = 0
    VOICE = 1
    CATEGORY = 2
    DIRECT = 3


class Status(IntEnum):
    OFFLINE = 0
    ONLINE = 1
    CONNECT = 2
    DISCONNECT = 3
    RECONNECT = 4


class MessageType(IntEnum):
    TEXT = 0
    IMAGE = 1
    VOICE = 2
    FILE = 3


class User:
    def __init__(self, user_info: dict):
        self.id: str = user_info.get('id', '')
        self.name: Optional[str] = user_info.get('name', '')
        self.avatar: Optional[str] = user_info.get('avatar', '')
        self.nick: Optional[str] = user_info.get('nick', '')
        self.is_bot: Optional[bool] = user_info.get('is_bot', False)


class Channel:
    def __init__(self, channel_info: dict):
        self.type: ChannelType = channel_info.get('type', ChannelType.TEXT)
        self.id: str = channel_info.get('id', '')
        self.name: Optional[str] = channel_info.get('name', '')
        self.parent_id: Optional[str] = channel_info.get('parent_id', '')


class Guild:
    def __init__(self, guild_info: dict):
        self.id: str = guild_info.get('id', '')
        self.name: Optional[str] = guild_info.get('name', '')
        self.avatar: Optional[str] = guild_info.get('avatar', '')


class Member:
    def __init__(self, member_info: dict):
        self.user: Optional[User] = User(member_info.get('user', {}))
        self.nick: Optional[str] = member_info.get('nick', '')
        self.avatar: Optional[str] = member_info.get('avatar', '')
        self.joined_at: Optional[int] = member_info.get('joined_at', '')


class Role:
    def __init__(self, role_info: dict):
        self.id: str = role_info.get('id', '')
        self.name: Optional[str] = role_info.get('name', '')


class Login:
    def __init__(self, login_info: dict):
        self.self_id: Optional[str] = login_info.get('self_id', '')
        self.platform: Optional[str] = login_info.get('platform', '')
        self.status: Status = login_info.get('status', Status.OFFLINE)
        self.user = User(login_info.get('user', {}))


class Message:
    def __init__(self, message_info: dict):
        self.id: str = message_info.get('id', '')
        self.content: str = message_info.get('content', '')
        self.member: Optional[Member] = Member(message_info.get('member', {}))
        self.user: Optional[User] = User(message_info.get('user', {}))
        self.channel: Optional[Channel] = Channel(message_info.get('channel', {}))
        self.guild: Optional[Guild] = Guild(message_info.get('guild', {}))
        self.created_at: Optional[int] = message_info.get('created_at', '')
        self.updated_at: Optional[int] = message_info.get('updated_at', '')

        self.quote: Quote = Quote(message_info.get('quote', {}))


class Quote:
    def __init__(self, quote_info: dict):
        self.id: Optional[str] = quote_info.get('id', '')
        self.message_id: Optional[str] = quote_info.get('message_id', '')
        self.content: Optional[str] = quote_info.get('content', '')
        self.user = User(quote_info.get('user', {}))


class Command:
    def __init__(self, command_name, args, text):
        self.command_name: str = command_name
        self.args: list = args
        self.text: str = text


class Session(Api):
    def __init__(self, body: dict):
        self.id: int = body.get('id', '')
        self.type: str = body.get('type', '')
        self.platform: str = body.get('platform', '')
        self.self_id: str = body.get('self_id', '')
        self.timestamp: int = body.get('timestamp', '')

        self.member: Optional[Member] = Member(body.get('member', {}))
        self.user: Optional[User] = User(body.get('user', {}))
        self.channel: Optional[Channel] = Channel(body.get('channel', {}))
        self.guild: Optional[Guild] = Guild(body.get('guild', {}))
        self.message: Optional[Message] = Message(body.get('message', {}))
        self.role: Optional[Role] = Role(body.get('role', {}))
        self.login: Optional[Login] = Login(body.get('login', {}))
        self.operator: Optional[User] = User(body.get('operator', {}))

        self.data: dict = body  # 原始数据
        self.command: Optional[Command] = None

        super().__init__(self.platform, self.self_id)
    #
    # def cmd(self, cmd: str) -> Command | bool:
    #     pure_message: str = rm_at_prefix(self.message.content)
    #     if pure_message.startswith(cmd + ' '):
    #         cmd_list: list = pure_message.split()
    #         args: list = cmd_list[1:]
    #         text: str = pure_message.replace(cmd, '', 1)
    #         if text.startswith(' '):
    #             text = text.replace(' ', '', 1)
    #         cmd_final = Command(cmd, args, text)
    #         return cmd_final
    #     if pure_message == cmd:
    #         cmd_final = Command(cmd, None, '')
    #         return cmd_final
    #     return False

    def send(self, message_content: str):
        print(f'[ send -> {self.platform}: {self.channel.name} ] ')
        return Api.message_create(self, channel_id=self.channel.id or self.guild.id, content=message_content)

    # message
    def message_create(self, channel_id: str = None, content: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        content = content or self.message.content
        message_id = message_id or self.message.id
        return super().message_create(channel_id, content, message_id)

    def message_get(self, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return super().message_get(channel_id, message_id)

    def message_delete(self, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return super().message_delete(channel_id, message_id)

    def message_update(self, channel_id: str = None, message_id: str = None, content: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        content = content or self.message.content
        return super().message_update(channel_id, message_id, content)

    def message_list(self, channel_id: str = None, next_token: str = None):
        channel_id = channel_id or self.channel.id
        return super().message_list(channel_id, next_token)

    def channel_get(self, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return super().channel_get(channel_id)

    def channel_list(self, guild_id: str = None, next_token: str = None):
        guild_id = guild_id or self.guild.id
        return super().channel_list(guild_id, next_token)

    def channel_create(self, guild_id: str = None, channel_data: dict = None):
        guild_id = guild_id or self.guild.id
        channel_data = channel_data or self.data.get('channel', {})
        return super().channel_create(guild_id, channel_data)

    def channel_update(self, channel_id: str = None, channel_data: dict = None):
        channel_id = channel_id or self.channel.id
        channel_data = channel_data or self.data.get('channel', {})
        return super().channel_update(channel_id, channel_data)

    def channel_delete(self, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return super().channel_delete(channel_id)

    def user_channel_create(self, user_id: str = None, guild_id: str = None):
        user_id = user_id or self.user.id
        guild_id = guild_id or self.guild.id
        return super().user_channel_create(user_id, guild_id)

    def guild_get(self, guild_id: str = None):
        guild_id = guild_id or self.guild.id
        return super().guild_get(guild_id)

    def guild_list(self, next_token: str = None):
        return super().guild_list(next_token)

    def guild_approve(self, message_id: str = None, approve: bool = False, comment: str = None):
        message_id = message_id or self.message.id
        return super().guild_approve(message_id, approve, comment)

    def guild_member_get(self, guild_id: str = None, user_id: str = None):
        guild_id = guild_id or self.guild.id
        user_id = user_id or self.user.id
        return super().guild_member_get(guild_id, user_id)

    def guild_member_list(self, guild_id: str = None, next_token: str = None):
        guild_id = guild_id or self.guild.id
        return super().guild_member_list(guild_id, next_token)

    def guild_member_kick(self, guild_id: str = None, user_id: str = None, permanent: bool = False):
        guild_id = guild_id or self.guild.id
        user_id = user_id or self.user.id
        return super().guild_member_kick(guild_id, user_id, permanent)

    def guild_member_approve(self, message_id: str = None, approve: bool = False, comment: str = None):
        message_id = message_id or self.message.id
        return super().guild_member_approve(message_id, approve, comment)

    def login_get(self):
        return super().login_get()

    def user_get(self, user_id: str = None):
        user_id = user_id or self.user.id
        return super().user_get(user_id)

    def friend_list(self, next_token: str = None):
        return super().friend_list(next_token)

    def friend_approve(self, message_id: str = None, approve: bool = False, comment: str = None):
        message_id = message_id or self.message.id
        return super().friend_approve(message_id, approve, comment)

    def reaction_create(self, channel_id: str = None, message_id: str = None, emoji: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return super().reaction_create(channel_id, message_id, emoji)

    def reaction_delete(self, channel_id: str = None, message_id: str = None, emoji: str = None, user_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        user_id = user_id or self.user.id
        return super().reaction_delete(channel_id, message_id, emoji, user_id)

    def reaction_clear(self, channel_id: str = None, message_id: str = None, emoji: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return super().reaction_clear(channel_id, message_id, emoji)

    def reaction_list(self, channel_id: str = None, message_id: str = None, emoji: str = None, next_token: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return super().reaction_list(channel_id, message_id, emoji, next_token)


def event_to_session(body_data: dict):
    session = Session(body_data)
    return session







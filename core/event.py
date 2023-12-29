from enum import IntEnum
from typing import Union, Optional

from request import send_request

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


class Event:
    def __init__(self, body=None):
        if body is None:
            body = {}
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
        self._type: str = body.get('_type', '')  # 内部
        self._data: dict = body.get('_data', {})  # 内部

        self.data: dict = body  # 原始数据

    # message
    def message_create(self,content: str = None, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return send_request(event=self, method='message.create', data={
            'channel_id': channel_id,
            'content': content,
        }, platform=self.platform, self_id=self.self_id)

    def message_delete(self, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return send_request(event=self, method='message.delete', data={
            'channel_id': channel_id,
            'message_id': message_id,
        }, platform=self.platform, self_id=self.self_id)

    def message_update(self, content: str = None, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return send_request(event=self, method='message.update', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'content': content,
        }, platform=self.platform, self_id=self.self_id)

    def message_list(self, next_token: str = None, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return send_request(event=self, method='message.list', data={
            'channel_id': channel_id,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def channel_get(self, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return send_request(event=self, method='channel.get', data={
            'channel_id': channel_id,
        }, platform=self.platform, self_id=self.self_id)

    def channel_list(self, next_token: str = None, guild_id: str = None):
        guild_id = guild_id or self.guild.id
        return send_request(event=self, method='channel.list', data={
            'guild_id': guild_id,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def channel_create(self, channel_data: dict = None, guild_id: str = None):
        guild_id = guild_id or self.guild.id
        return send_request(event=self, method='channel.create', data={
            'guild_id': guild_id,
            'data': channel_data,
        }, platform=self.platform, self_id=self.self_id)

    def channel_update(self, channel_data: dict = None, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return send_request(event=self, method='channel.update', data={
            'channel_id': channel_id,
            'data': channel_data,
        }, platform=self.platform, self_id=self.self_id)

    def channel_delete(self, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return send_request(event=self, method='channel.delete', data={
            'channel_id': channel_id,
        }, platform=self.platform, self_id=self.self_id)

    def guild_get(self, guild_id: str = None):
        guild_id = guild_id or self.guild.id
        return send_request(event=self, method='guild.get', data={
            'guild_id': guild_id,
        }, platform=self.platform, self_id=self.self_id)

    def guild_list(self, next_token: str = None):
        return send_request(event=self, method='guild.list', data={
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def guild_approve(self, approve: bool = False, comment: str = None, message_id: str = None):
        message_id = message_id or self.message.id
        return send_request(event=self, method='guild.approve', data={
            'message_id': message_id,
            'approve': approve,
            'comment': comment,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_get(self, guild_id: str = None, user_id: str = None):
        guild_id = guild_id or self.guild.id
        user_id = user_id or self.user.id
        return send_request(event=self, method='guild.member.get', data={
            'guild_id': guild_id,
            'user_id': user_id,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_list(self, next_token: str = None, guild_id: str = None):
        guild_id = guild_id or self.guild.id
        return send_request(event=self, method='guild.member.list', data={
            'guild_id': guild_id,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_kick(self, permanent: bool = False, guild_id: str = None, user_id: str = None):
        guild_id = guild_id or self.guild.id
        user_id = user_id or self.user.id
        return send_request(event=self, method='guild.member.kick', data={
            'guild_id': guild_id,
            'user_id': user_id,
            'permanent': permanent,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_approve(self, approve: bool = False, comment: str = None, message_id: str = None):
        message_id = message_id or self.message.id
        return send_request(event=self, method='guild.member.approve', data={
            'message_id': message_id,
            'approve': approve,
            'comment': comment,
        }, platform=self.platform, self_id=self.self_id)

    def login_get(self):
        return send_request(event=self, method='login.get', data={}, platform=self.platform, self_id=self.self_id)

    def user_get(self, user_id: str = None):
        user_id = user_id or self.user.id
        return send_request(event=self, method='user.get', data={
            'user_id': user_id,
        }, platform=self.platform, self_id=self.self_id)

    def friend_list(self, next_token: str = None):
        return send_request(event=self, method='friend.list', data={
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def friend_approve(self, approve: bool = False, comment: str = None, message_id: str = None):
        message_id = message_id or self.message.id
        return send_request(event=self, method='friend.approve', data={
            'message_id': message_id,
            'approve': approve,
            'comment': comment,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_create(self, emoji: str = None, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return send_request(event=self, method='reaction.create', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_delete(self, emoji: str = None, user_id: str = None, channel_id: str = None, message_id: str = None):
        user_id = user_id or self.user.id
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return send_request(event=self, method='reaction.delete', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
            'user_id': user_id,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_clear(self, emoji: str = None, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return send_request(event=self, method='reaction.clear', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_list(self, emoji: str = None, next_token: str = None, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return send_request(event=self, method='reaction.list', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)


class SessionInternal:
    def __init__(self, body=None):
        '''
        内部使用的 Session
        # 字段	类型	说明
        # id	number	事件 ID
        # type	string	事件类型 (固定为 internal)
        # platform	string	接收者的平台名称
        # self_id	string	接收者的平台账号
        # timestamp	number	事件的时间戳
        # _type	string	原生事件类型
        # _data	object	原生事件数据
        '''
        if body is None:
            body = {}
        self.id: int = body.get('id', '')
        self.type: str = body.get('type', '')
        self.platform: str = body.get('platform', '')
        self.self_id: str = body.get('self_id', '')
        self.timestamp: int = body.get('timestamp', '')

        self._type: str = body.get('_type', '')
        self._data: dict = body.get('_data', {})














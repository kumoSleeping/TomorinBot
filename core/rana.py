import base64
import io
from PIL import Image
from enum import IntEnum
from typing import Union, Optional

from soyorin import Utils
from rikki import Rikki

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
        self.user: Optional[User] = User(member_info.get('user'))
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
        self.channel: Optional[User] = Channel(message_info.get('channel', {}))
        self.guild: Optional[Guild] = Guild(message_info.get('guild', {}))
        self.created_at: Optional[int] = message_info.get('created_at', '')
        self.updated_at: Optional[int] = message_info.get('updated_at', '')


class Session:
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

    def send(self, message_content: str):
        return Rikki.send_request(method='message.create', data={
            'channel_id': self.channel.id,
            'content': message_content
        }, platform=self.platform, self_id=self.self_id)

    def call_api(self, method: str, data):
        return Rikki.send_request(method=method, data=data, platform=self.platform, self_id=self.self_id)


# 解析收到的消息信息
def parse_message(message_info: dict):
    session = Session(message_info)
    return session


class Rana:
    @staticmethod
    def process_satori_message(body_data: dict):
        session = parse_message(body_data)
        # 控制台输出
        try:
            Utils.show_session_log(session)
        except Exception as e:
            print(f'[Error] Rana 抛出 {e}')
        return session


class H:
    @staticmethod
    def text(content: str):
        return f'<content>{content}</content>'

    @staticmethod
    def at(user_id: Union[int, str]):
        return f'<at id="{user_id}"/>'

    @staticmethod
    def sharp(channel_id: Union[int, str]):
        return f'<sharp id="{channel_id}"/>'

    @staticmethod
    def quote(message_id: Union[int, str]):
        return f'<quote id="{message_id}"/>'

    @staticmethod
    def image(param: Union[Image.Image, bytes, str]):
        if isinstance(param, Image.Image):
            print("这是一个Pillow图像对象")
            with io.BytesIO() as output:
                param.save(output, format='PNG')
                image_binary = output.getvalue()
            # 将二进制数据转换为Base64编码
            encoded_image = base64.b64encode(image_binary).decode('utf-8')
            # 构建XML格式字符串
            return f'<image url="data:image/png;base64,{encoded_image}"/>'
        elif isinstance(param, bytes):
            encoded_image = base64.b64encode(param).decode('utf-8')
            print("这是一个bytes")
            return f'<image url="data:image/png;base64,{encoded_image}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                print("这是一个字符串")
                return f'<image url="{param}"/>'

    @staticmethod
    def audio(param: Union[bytes, str]):
        if isinstance(param, bytes):
            encoded_audio = base64.b64encode(param).decode('utf-8')
            return f'<audio url="data:audio/mpeg;base64,{encoded_audio}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<audio url="{param}"/>'

    @staticmethod
    def video(param: Union[bytes, str]):
        if isinstance(param, bytes):
            encoded_video = base64.b64encode(param).decode('utf-8')
            return f'<video url="data:video/mp4;base64,{encoded_video}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<video url="{param}"/>'

    @staticmethod
    def file(param: Union[bytes, str]):
        if isinstance(param, bytes):
            encoded_file = base64.b64encode(param).decode('utf-8')
            return f'<file url="data:application/octet-stream;base64,{encoded_file}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<file url="{param}"/>'


h = H()



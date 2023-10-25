import base64
import io
from PIL import Image


from soyorin import Utils
from rikki import Rikki

'''
Rana.py
对「satori」协议进行基础消息抽象 / 日志显示
提供平台包装元素的 API
'''


class User:
    def __init__(self, user_info):
        self.id = user_info.get('id', '')
        self.name = user_info.get('name', '')
        self.avatar = user_info.get('avatar', '')
        self.nick = user_info.get('nick', '')
        self.is_bot = user_info.get('is_bot', '')


class Channel:
    def __init__(self, channel_info):
        self.type = channel_info.get('type', '')
        self.id = channel_info.get('id', '')
        self.name = channel_info.get('name', '')
        self.parent_id = channel_info.get('parent_id', '')


class Guild:
    def __init__(self, guild_info):
        self.id = guild_info.get('id', '')
        self.name = guild_info.get('name', '')
        self.avatar = guild_info.get('avatar', '')


class Member:
    def __init__(self, member_info):
        self.user = member_info.get('user', '')
        self.nick = member_info.get('nick', '')
        self.avatar = member_info.get('avatar', '')
        self.joined_at = member_info.get('joined_at', '')
        self.user = User(member_info.get('user', {}))


class Operator:
    def __init__(self, operator_info):
        self.id = operator_info.get('id', '')
        self.name = operator_info.get('name', '')
        self.avatar = operator_info.get('avatar', '')
        self.nick = operator_info.get('nick', '')
        self.is_bot = operator_info.get('is_bot', '')


class Role:
    def __init__(self, role_info):
        self.id = role_info.get('id', '')
        self.name = role_info.get('name', '')


class Login:
    def __init__(self, login_info):
        self.id = login_info.get('id', '')
        self.self_id = login_info.get('self_id', '')
        self.platform = login_info.get('platform', '')
        self.status: int = login_info.get('status', '')
        self.user = User(login_info.get('user', {}))


class Message:
    def __init__(self, message_info):
        self.id = message_info.get('id', '')
        self.content = message_info.get('content', '')
        self.member = Member(message_info.get('member', {}))
        self.user = User(message_info.get('user', {}))
        self.channel = Channel(message_info.get('channel', {}))
        self.guild = Guild(message_info.get('guild', {}))
        self.created_at: int = message_info.get('created_at', '')
        self.updated_at: int = message_info.get('updated_at', '')


class Session:
    def __init__(self, body):
        self.id = body.get('id', '')
        self.type = body.get('type', '')
        self.platform = body.get('platform', '')
        self.self_id = body.get('self_id', '')
        self.timestamp = body.get('timestamp', '')
        self.subtype = body.get('subtype', '')

        self.member = Member(body.get('member', {}))
        self.user = User(body.get('user', {}))
        self.channel = Channel(body.get('channel', {}))
        self.guild = Guild(body.get('guild', {}))
        self.message = Message(body.get('message', {}))
        self.guild = Guild(body.get('guild', {}))
        self.message = Message(body.get('message', {}))
        self.role = Role(body.get('role', {}))
        self.login = Login(body.get('login', {}))
        self.operator = Operator(body.get('operator', {}))

    def send(self, message_content):
        return Rikki.send_request(method='message.create', data={
            'channel_id': self.channel.id,
            'content': message_content
        }, platform=self.platform, self_id=self.self_id)

    def call_api(self, method, data):
        return Rikki.send_request(method=method, data=data, platform=self.platform, self_id=self.self_id)


# 解析收到的消息信息
def parse_message(message_info):
    session = Session(message_info)
    return session


class Rana:
    @staticmethod
    def process_satori_message(body_data):
        session = parse_message(body_data)
        # 控制台输出
        try:
            Utils.show_session_log(session)
        except Exception as e:
            print(f'[Error] Rana 抛出 {e}')
        return session


class H:
    @staticmethod
    def text(content):
        return f'<content>{content}</content>'

    @staticmethod
    def at(user_id):
        return f'<at id="{user_id}"/>'

    @staticmethod
    def sharp(channel_id):
        return f'<sharp id="{channel_id}"/>'

    @staticmethod
    def quote(message_id):
        return f'<quote id="{message_id}"/>'

    @staticmethod
    def image(param):
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
    def audio(param):
        if isinstance(param, bytes):
            encoded_audio = base64.b64encode(param).decode('utf-8')
            return f'<audio url="data:audio/mpeg;base64,{encoded_audio}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<audio url="{param}"/>'

    @staticmethod
    def video(param):
        if isinstance(param, bytes):
            encoded_video = base64.b64encode(param).decode('utf-8')
            return f'<video url="data:video/mp4;base64,{encoded_video}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<video url="{param}"/>'

    @staticmethod
    def file(param):
        if isinstance(param, bytes):
            encoded_file = base64.b64encode(param).decode('utf-8')
            return f'<file url="data:application/octet-stream;base64,{encoded_file}"/>'
        else:
            if str(param).startswith("http://") or str(param).startswith("https://"):
                return f'<file url="{param}"/>'


h = H()



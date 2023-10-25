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
        self.user_id = user_info.get('user_id', '')
        self.avatar = user_info.get('avatar', '')
        self.username = user_info.get('username', '')


class Channel:
    def __init__(self, channel_info):
        self.type = channel_info.get('type', '')
        self.id = channel_info.get('id', '')
        self.name = channel_info.get('name', '')


class Guild:
    def __init__(self, guild_info):
        self.id = guild_info.get('id', '')
        self.name = guild_info.get('name', '')
        self.avatar = guild_info.get('avatar', '')


class Member:
    def __init__(self, member_info):
        self.name = member_info.get('name', '')
        self.roles: list = member_info.get('roles', '')

        self.member_user = MemberUser(member_info.get('user', {}))


class MemberUser:
    def __init__(self, member_user_info):
        self.id = member_user_info.get('id', '')
        self.name = member_user_info.get('name', '')
        self.user_id = member_user_info.get('user_id', '')
        self.avatar = member_user_info.get('avatar', '')
        self.username = member_user_info.get('username', '')


class Message:
    def __init__(self, message_info):
        self.id = message_info.get('id', '')
        self.content = message_info.get('content', '')

        self.elements = Elements(message_info.get('elements', []))


class Elements:
    def __init__(self, elements_info):
        self.types = []  # 存储类型的列表
        self.attrs_list = []  # 存储attrs的列表
        self.children_list = []  # 存储children的列表

        for element_data in elements_info:
            element_type = element_data.get('type', '')
            element_attrs = element_data.get('attrs', {})
            element_children = element_data.get('children', [])

            self.types.append(element_type)
            self.attrs_list.append(element_attrs)
            self.children_list.append(element_children)


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

        self.member_user = MemberUser(body.get('message', {}))


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



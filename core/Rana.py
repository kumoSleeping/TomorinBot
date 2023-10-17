from core.Soyorin import Utils
import base64, io

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
    def __init__(self, guild_info):
        self.name = guild_info.get('name', '')


class Message:
    def __init__(self, message_info):
        self.id = message_info.get('id', '')
        self.content = message_info.get('content', '')
        self.elements = message_info.get('elements', '')


class Session:
    def __init__(self, body):
        self.id = body.get('id', '')
        self.type = body.get('type', '')
        self.platform = body.get('platform', '')
        self.self_id = body.get('self_id', '')
        self.timestamp = body.get('timestamp', '')
        self.user = User(body.get('user', {}))
        self.channel = Channel(body.get('channel', {}))
        self.guild = Guild(body.get('guild', {}))
        self.member = body.get('member', {})
        self.message = Message(body.get('message', {}))


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
    def image_url(url):
        return f'<image url="{url}"/>'

    @staticmethod
    def audio_url(url):
        return f'<audio url="{url}"/>'

    @staticmethod
    def video_url(url):
        return f'<video url="{url}"/>'

    @staticmethod
    def file_url(url):
        return f'<file url="{url}"/>'

    @staticmethod
    def image_buffer(buffer, mime_type='image/png'):
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        return f'<image type="{mime_type}" data="{encoded_image}"/>'

    @staticmethod
    def image_pil(image, mime_type='image/png'):
        # 将Pillow Image对象转换为二进制数据
        with io.BytesIO() as output:
            image.save(output, format='PNG')
            image_binary = output.getvalue()

        # 将二进制数据转换为Base64编码
        encoded_image = base64.b64encode(image_binary).decode('utf-8')

        # 构建XML格式字符串
        return f'<image url="data:{mime_type};base64,{encoded_image}"/>'

    @staticmethod
    def audio_buffer(buffer, mime_type='audio/mpeg'):
        encoded_audio = base64.b64encode(buffer).decode('utf-8')
        return f'<audio type="{mime_type}" data="{encoded_audio}"/>'

    @staticmethod
    def video_buffer(buffer, mime_type='video/mp4'):
        encoded_video = base64.b64encode(buffer).decode('utf-8')
        return f'<video type="{mime_type}" data="{encoded_video}"/>'

    @staticmethod
    def file_buffer(buffer, mime_type='application/octet-stream'):
        encoded_file = base64.b64encode(buffer).decode('utf-8')
        return f'<file type="{mime_type}" data="{encoded_file}"/>'


h = H()



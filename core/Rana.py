from .utils.utils import Utils

'''
Rana.py
对「satori」协议进行基础消息抽象 / 日志显示
提供平台包装元素的 API
'''


class User:
    def __init__(self, user_info):
        self.id = user_info.get('id')
        self.name = user_info.get('name')
        self.avatar = user_info.get('avatar')


class Channel:
    def __init__(self, channel_info):
        self.type = channel_info.get('type')
        self.id = channel_info.get('id')
        self.name = channel_info.get('name')


class Guild:
    def __init__(self, guild_info):
        self.id = guild_info.get('id')
        self.name = guild_info.get('name')
        self.avatar = guild_info.get('avatar')


class Member:
    def __init__(self, guild_info):
        self.name = guild_info.get('name')


class Message:
    def __init__(self, message_info):
        self.id = message_info.get('id')
        self.content = message_info.get('content')


class Session:
    def __init__(self, body):
        self.id = body.get('id')
        self.type = body.get('type')
        self.platform = body.get('platform')
        self.self_id = body.get('self_id')
        self.timestamp = body.get('timestamp')
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


import re

'''
Rana.py
对「satori」协议进行基础消息抽象 / 日志显示
提供平台包装元素的 API
'''


class RanaUtils:
    @staticmethod
    def escape_special_characters(message):
        # 替换特殊字符为转义字符
        message = message.replace('"', '&quot;')
        message = message.replace('&', '&amp;')
        message = message.replace('<', '&lt;')
        message = message.replace('>', '&gt;')
        return message

    @staticmethod
    def show_log(session):
        # 展示日志
        message_content = session.message.content

        html_tag_pattern = re.compile(r'<.*?>')
        # 将所有HTML标签替换为占位符
        cleaned_text = re.sub(html_tag_pattern, '[xml元素]', message_content)
        cleaned_text = cleaned_text[0:15] + '...' if len(cleaned_text) > 15 else cleaned_text

        user_id = session.user.id
        try:
            member = session.user.name
            if not member:
                member = f'QQ用户{user_id}'
        except:
            # 为什么是QQ用户，因为就QQ可能拿不到成员name...
            member = f'QQ用户{user_id}'
        print(f"[ {session.guild.name} ] （ {member} ）{cleaned_text}")


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


def process_satori_message(body_data):

    session = parse_message(body_data)

    # try:
    # 控制台输出
    try:
        RanaUtils.show_log(session)
    except Exception as e:
        print(f'[Error] Rana 抛出 {e}')
    return session
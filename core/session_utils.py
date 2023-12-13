import re
import json
from config import config


def show_session_log(session):
    # 展示日志
    message_content = session.message.content

    html_tag_pattern = re.compile(r'<.*?>')
    # 将所有HTML标签替换为占位符
    cleaned_text = re.sub(html_tag_pattern, '[媒体消息]', message_content)
    cleaned_text = cleaned_text[0:15] + '...' if len(cleaned_text) > 15 else cleaned_text
    cleaned_text = cleaned_text.replace("\n", " ").replace("\r", " ")

    user = session.user.name if session.user.name != '' else ('U_' + session.user.id)
    guild = session.guild.name if session.guild.name != '' else ('G_' + session.guild.id)
    channel = session.channel.name if session.channel.name != '' else ('G_' + session.channel.id)
    place = channel if channel == guild else guild + '->' + channel
    if session.type != 'internal':
        print(f"[ {session.platform}: {place} ] < {session.type} >（ {user} ）{cleaned_text}")


def show_session_data(data: dict):
    if config['server']['reload']:
        pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
        print(pretty_json)
import re
import json
from config import config


def show_session_log(session: "Session"):
    # 展示日志
    message_content = session.message.content

    html_tag_pattern = re.compile(r'<.*?>')
    # 将所有HTML标签替换为占位符
    cleaned_text = re.sub(html_tag_pattern, '[xml元素]', message_content)
    cleaned_text = cleaned_text[0:15] + '...' if len(cleaned_text) > 15 else cleaned_text
    cleaned_text = cleaned_text.replace("\n", " ").replace("\r", " ")

    member = session.user.name
    if not member:
        # 为什么 因为QQ可能拿不到成员name...
        member = f'用户{session.user.id}'

    try:
        group = session.guild.name
        if not group:
            group = f'频道: {session.channel.name}'
    except:
        # 为什么是QQ用户，因为就QQ可能拿不到成员name...
        group = f'用户{session.user.id}'

    print(f"[ {session.platform}: {group} ] （ {member} ）{cleaned_text}")


def show_session_data(data: dict):
    if config['server']['reload']:
        pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
        print(pretty_json)
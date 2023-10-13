import re


class Utils:
    @staticmethod
    def escape_special_characters(message):
        # 替换特殊字符为转义字符
        message = message.replace('"', '&quot;')
        message = message.replace('&', '&amp;')
        message = message.replace('<', '&lt;')
        message = message.replace('>', '&gt;')
        return message

    @staticmethod
    def unescape_special_characters(escaped_message):
        # 将转义字符替换回特殊字符
        escaped_message = escaped_message.replace('&quot;', '"')
        escaped_message = escaped_message.replace('&amp;', '&')
        escaped_message = escaped_message.replace('&lt;', '<')
        escaped_message = escaped_message.replace('&gt;', '>')
        return escaped_message

    @staticmethod
    def show_session_log(session):
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


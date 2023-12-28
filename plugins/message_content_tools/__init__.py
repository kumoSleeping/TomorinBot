import re

from core import config


def escape_satori_special_characters(message: str):
    # 替换特殊字符为转义字符
    message = message.replace('&', '&amp;')
    message = message.replace('"', '&quot;')
    message = message.replace('<', '&lt;')
    message = message.replace('>', '&gt;')
    return message


def unescape_satori_sspecial_characters(escaped_message: str):
    # 将转义字符替换回特殊字符
    escaped_message = escaped_message.replace('&quot;', '"')
    escaped_message = escaped_message.replace('&amp;', '&')
    escaped_message = escaped_message.replace('&lt;', '<')
    escaped_message = escaped_message.replace('&gt;', '>')
    return escaped_message


def remove_first_at_xml(text):
    clean_text = re.sub(r'<at.*?>', '', text, count=1)  # 使用 count=1 只替换第一个匹配项
    return clean_text.strip()


def remove_all_at_xml(text):
    clean_text = re.sub(r'<at.*?>', '', text)
    return clean_text.strip()


def remove_all_xml(text):
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text.strip()


def remove_first_prefix(text):
    for prefix in config['message_content_tools']['prefix']:
        if text.startswith(prefix):
            text = text.replace(prefix, '', 1)
            break
    return text.strip()


def plaintext_if_prefix(text):
    for prefix in config['message_content_tools']['prefix']:
        if text.startswith(prefix):
            text = text.replace(prefix, '', 1)
            return text.strip()
    else:
        text = ''
        return text


def easy_to_show_text(text):
    html_tag_pattern = re.compile(r'<.*?>')
    # 将所有HTML标签替换为占位符
    cleaned_text = re.sub(html_tag_pattern, '[媒体消息]', text)
    cleaned_text = cleaned_text[0:15] + '...' if len(cleaned_text) > 15 else cleaned_text
    cleaned_text = cleaned_text.replace("\n", " ").replace("\r", " ")
    return cleaned_text


import json
import re


def escape_special_characters(message: str):
    # 替换特殊字符为转义字符
    message = message.replace('&', '&amp;')
    message = message.replace('"', '&quot;')
    message = message.replace('<', '&lt;')
    message = message.replace('>', '&gt;')
    return message


def unescape_special_characters(escaped_message: str):
    # 将转义字符替换回特殊字符
    escaped_message = escaped_message.replace('&quot;', '"')
    escaped_message = escaped_message.replace('&amp;', '&')
    escaped_message = escaped_message.replace('&lt;', '<')
    escaped_message = escaped_message.replace('&gt;', '>')
    return escaped_message


def rm_1_at(text):
    clean_text = re.sub(r'<at.*?>', '', text, count=1)  # 使用 count=1 只替换第一个匹配项
    return clean_text.strip()


def rm_at_prefix(text):
    clean_text = re.sub(r'<at.*?>', '', text, count=1)  # 使用 count=1 只替换第一个匹配项
    if clean_text.strip().startswith('/'):
        clean_text = clean_text.replace('/', '', 1).strip()
    return clean_text



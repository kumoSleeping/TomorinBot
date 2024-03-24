import re

from mods import config
from mods import log

config.need('message_content_tools', {'prefix': ['/', '']})

if '' not in config.get_key('message_content_tools').get('prefix'):
    log.warning('\033[33m[message_content_tools] 不存在空前缀，可能导致一些命令被拦截\033[0m')
# 如果存在，检查是否在最后
elif config.get_key('message_content_tools').get('prefix')[-1] != '':
    log.warning('\033[33m[message_content_tools] 空前缀不在最后，后续前缀将失效\033[0m')


def escape_satori_special_characters(message: str):
    '''
    替换特殊字符为转义字符 (对于satori协议)


    Replace special characters with escape characters (for the satori protocol)
    '''
    message = message.replace('&', '&amp;')
    message = message.replace('"', '&quot;')
    message = message.replace('<', '&lt;')
    message = message.replace('>', '&gt;')
    return message


def unescape_satori_special_characters(escaped_message: str):
    '''
    替换转义字符为特殊字符 (对于satori协议)


    Replace escape characters with special characters (for the satori protocol)
    '''
    escaped_message = escaped_message.replace('&quot;', '"')
    escaped_message = escaped_message.replace('&amp;', '&')
    escaped_message = escaped_message.replace('&lt;', '<')
    escaped_message = escaped_message.replace('&gt;', '>')
    return escaped_message


def remove_first_at_xml(text):
    '''
    移除第一个xml标签


    Remove the first xml tag
    '''
    clean_text = re.sub(r'<at.*?>', '', text, count=1)  # 使用 count=1 只替换第一个匹配项
    return clean_text.strip()


def remove_all_at_xml(text):
    '''
    移除所有xml标签


    Remove all xml tags
    '''
    clean_text = re.sub(r'<at.*?>', '', text)
    return clean_text.strip()


def remove_all_xml(text):
    '''
    移除所有xml标签


    Remove all xml tags
    '''
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text.strip()


def remove_first_prefix(text):
    '''
    移除第一个前缀 (前缀在配置文件规定)


    Remove the first prefix (the prefix is specified in the configuration file)
    '''
    for prefix in config.get_key('message_content_tools').get('prefix'):
        if text.startswith(prefix):
            text = text.replace(prefix, '', 1)
            break
    return text.strip()


def plaintext_if_prefix(text):
    '''
    如果有前缀，移除第一个前缀 (前缀在配置文件规定)，如果没有前缀，返回空字符串


    If there is a prefix, remove the first prefix (the prefix is specified in the configuration file), if there is no prefix, return an empty string
    '''
    for prefix in config.get_key('message_content_tools').get('prefix'):
        text = remove_all_xml(text)
        if text.startswith(prefix):
            text = text.replace(prefix, '', 1)
            return text.strip()
    else:
        text = ''
        return text


def easy_to_show_text(text):
    '''
    获得易于显示的文本 (简化收到的消息便于打印)


    Get text that is easy to display (simplify the received message for printing)
    '''
    html_tag_pattern = re.compile(r'<.*?>')
    # 将所有HTML标签替换为占位符
    cleaned_text = re.sub(html_tag_pattern, '[媒体消息]', text)
    cleaned_text = cleaned_text[0:15] + '...' if len(cleaned_text) > 15 else cleaned_text
    cleaned_text = cleaned_text.replace("\n", " ").replace("\r", " ")
    return cleaned_text






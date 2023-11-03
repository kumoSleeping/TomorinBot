import time
import re

from core.rana import h


def echo(session):
    """
    回声
    复读你的话
    """
    def rm_xml(text):
        clean_text = re.sub(r'<at.*?>', '', text, count=1)  # 使用 count=1 只替换第一个匹配项
        return clean_text

    pure_msg = rm_xml(session.message.content).strip()
    if pure_msg.startswith('echo '):
        session.send(pure_msg[5:])


def echoo(session):
    """
    很拖拉的回声
    复读你的话，但是等五秒
    """
    if str(session.message.content).startswith('echoo '):
        time.sleep(5)
        session.send(session.message.content[6:])





import time
import re

from core.rana import h
from core.soyorin import Utils


def echo(session):
    """
    回声
    复读你的话
    """

    pure_msg = Utils.rm_1_at(session.message.content).strip()
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



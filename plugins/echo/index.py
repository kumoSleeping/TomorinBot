import time
import re

from core.tomorin import h, rm_1_at, api


def echo(session):
    """
    回声
    复读你的话
    """

    pure_msg = rm_1_at(session.message.content).strip()
    if pure_msg.startswith('echo '):
        session.send(pure_msg[5:])


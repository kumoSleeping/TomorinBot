import time

from core.Rana import h


def echo(session):
    """
    回声
    复读你的话
    """
    if session.user.id not in ['1528593481']:
        return
    if str(session.message.content).startswith('echo '):
        # time.sleep(5)
        rpl = session.message.content[5:]
        session.send(rpl)


def echoo(session):
    """
    很拖拉的回声
    复读你的话，但是等五秒
    """
    if session.user.id not in ['1528593481']:
        return

    if str(session.message.content).startswith('echoo '):
        time.sleep(5)
        rpl = session.message.content[6:]
        session.send(rpl)


def test2(session):
    if session.message.content == '测试音频':
        session.send(f'{h.audio("https://bestdori.com/assets/jp/sound/bgm542_rip/bgm542.mp3")}')
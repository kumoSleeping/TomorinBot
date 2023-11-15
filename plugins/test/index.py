import time

from core.tomorin import h


def test(session):
    """
    测你的码
    喵 发送ttt
    """
    if session.message.content == 'ttt':
        session.send('tt你的bb')


def test2(session):
    '''
    测试音频
    查曲 542
    '''
    if session.message.content == '测试音频':
        session.send(f'{h.audio("https://bestdori.com/assets/jp/sound/bgm542_rip/bgm542.mp3")}')







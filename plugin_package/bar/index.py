from core.Rana import Rana, h
from core.Rikki import Rikki, send


def src(session):
    if session.message.content == '测试111':
        # image = Image.new('RGB', (50, 50), color='red')
        send(f'{h.quote(session.message.id)} {h.at(session.user.id)} 没有色图', session)



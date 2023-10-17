from core.Rana import Rana, h
from core.Rikki import Rikki, send


def src(session):
    if session.message.content == 'foo':
        send(f'{h.quote(session.message.id)} {h.at(session.user.id)} bar', session)

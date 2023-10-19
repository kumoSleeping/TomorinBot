import time

from core.Rana import h
from core.Rikki import send, in_api


def src(session):
    if session.message.content == 'foo':
        send(f'bar', session)

        # rpl = in_api('guild.member.get', {"guild_id": session.guild.id, "user_id": session.user.id}, session)
        # print(rpl)
        # rpl = in_api('guild.member.list', {"guild_id": session.guild.id, "next": "0"}, session)
        # print(rpl)
        # rpl = in_api('message.list', {"channel_id": session.channel.id, "next": "0"}, session)
        # print(rpl)
        # msg_id = send(f'{h.quote(session.message.id)} {h.at(session.user.id)} bar', session)[0]
        # print(msg_id)
        # time.sleep(3)
        # rpl = in_api('message.delete', {"message_id": msg_id, "channel_id": session.channel.id}, session)
        # print(rpl)

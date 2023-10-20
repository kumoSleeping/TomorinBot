import time

from core.Rana import h


def src(session):
    if session.message.content == 'foo':
        # 使用xml元素提及用户，正常推荐使用 h.at(session.user.id)
        msg_id = session.send(f'<at id="{session.user.id}"/> bar')

        time.sleep(3)
        # 尝试撤回消息（前提是平台支持这个API）
        rpl = session.call_api(method='message.delete', data={"message_id": msg_id, "channel_id": session.channel.id})
        # print(rpl)

import random


def qq_passive__(action, mseeage_content: str):
    try:
        if action.event.type == 'message-created' and action.event.platform in ['qq', 'qqguild'] and '<passive id=' not in action.event.message.content:
            seq = random.randint(1, 2147483640)
            if action.seq == 0:
                action.seq = seq
            else:
                seq = action.seq + 1
            mseeage_content += f'<passive id="{action.event.message.id}" seq="{seq}"/>'
    except:
        pass
    return mseeage_content






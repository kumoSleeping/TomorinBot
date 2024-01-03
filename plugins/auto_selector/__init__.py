from core import on, Event
from plugins.message_content_tools import plaintext_if_prefix, remove_all_xml, remove_first_prefix


class ASC:
    def __init__(self, event: Event, args: list, text: str):
        self.event: Event = event
        self.args: list = args
        self.text: str = text

    def send(self, content: str):
        return self.event.message_create(content=content)


def asc(event, command: list, prefix: bool = True):
    pure_msg = event.message.content
    # 如果at的xml元素存在于消息
    if f'<at id="{event.self_id}' not in pure_msg and ('<at id="' in pure_msg and '"/>' in pure_msg):
        pure_msg = ''
    if prefix:
        pure_msg = plaintext_if_prefix(pure_msg).strip()
    else:
        pure_msg = remove_all_xml(remove_first_prefix(pure_msg)).strip()
    if pure_msg == '':
        return None
    for item in command:
        cmd = pure_msg.split()[0] if len(pure_msg.split()) > 0 else ''
        if item.startswith(cmd + ' '):
            args = pure_msg.split()[1:]
            text = pure_msg.replace(cmd + ' ', '', 1)
            return ASC(event, args, text)
        elif item == cmd:
            args = pure_msg.split()[1:]
            text = pure_msg.replace(cmd + ' ', '', 1)
            return ASC(event, args, text)
    return None

from core import on, Event
from typing import Optional, Union, List
from plugins.message_content_tools import plaintext_if_prefix, remove_all_xml, remove_first_prefix
from plugins.auth import is_admin


class ASC:
    def __init__(self, event: Event, args: list, text: str):
        self.event: Event = event
        self.args: list = args
        self.text: str = text

    def send(self, content: str):
        return self.event.message_create(content=content)


def asc(event, command: Optional[Union[List[str], str]] = None, startswith: bool = False, force_prefix: bool = False,
        no_args: bool = False, admin: bool = False) -> Optional[ASC]:
    if admin:
        if not is_admin(event.platform, event.user.id):
            return None
    pure_msg = event.message.content
    # 如果at的xml元素存在于消息
    if f'<at id="{event.self_id}' not in pure_msg and ('<at id="' in pure_msg and '"/>' in pure_msg):
        pure_msg = ''
    if force_prefix:
        pure_msg = plaintext_if_prefix(pure_msg).strip()
    else:
        pure_msg = remove_all_xml(remove_first_prefix(pure_msg)).strip()
    if pure_msg == '':
        return None
    if isinstance(command, str):
        command: list = [command]
    for item in command:
        # cmd = pure_msg.split()[0] if len(pure_msg.split()) > 0 else ''
        if pure_msg.startswith(item + ' ') and no_args is False:
            args = pure_msg.split()[1:]
            text = pure_msg.replace(item + ' ', '', 1)
            return ASC(event, args, text)
        elif startswith and pure_msg.startswith(item) and no_args is False:
            args = pure_msg.replace(item, '', 1).split()
            text = pure_msg.replace(item, '', 1)
            return ASC(event, args, text)
        elif pure_msg == item:
            return ASC(event, [], '')

    return None

from core import on, Event
from typing import Optional, Union, List
from plugins.message_content_tools import plaintext_if_prefix, remove_all_xml, remove_first_prefix
from plugins.auth import is_admin


class MC:
    def __init__(self, event: Event, args: list, text: str):
        self.event: Event = event
        self.args: list = args
        self.text: str = text

    def send(self, content: str):
        return self.event.message_create(content=content)


def match_command(event, command: Optional[Union[List[str], str]] = None,
                  gap_less: bool = False, arg_less: bool = False, admin_only: bool = False,
                  match_args: Optional[Union[List[str], str]] = None,
                  match_text: str = None) -> Optional[MC]:
    if admin_only:
        if not is_admin(event.platform, event.user.id):
            return None

    pure_msg = event.message.content

    if f'<at id="{event.self_id}' not in pure_msg and ('<at id="' in pure_msg and '"/>' in pure_msg):
        pure_msg = ''

    pure_msg = plaintext_if_prefix(pure_msg).strip()

    if pure_msg == '':
        return None

    if isinstance(command, str):
        command: list = [command]

    for item in command:
        if pure_msg.startswith(item + ' ') and not arg_less:
            args = pure_msg.split()[1:]
            text = pure_msg.replace(item + ' ', '', 1)
        elif gap_less and pure_msg.startswith(item) and not arg_less:
            args = pure_msg.replace(item, '', 1).split()
            text = pure_msg.replace(item, '', 1)
        elif pure_msg == item:
            args = []
            text = ''
        else:
            continue

        # Check for match_args
        args_match = False
        if match_args is not None:
            if isinstance(match_args, str):
                match_args = [match_args]
            args_match = any(arg in match_args for arg in args)

        # Check for match_text
        text_match = match_text is not None and match_text in text

        # Return MC if either condition is satisfied
        if args_match or text_match:
            return MC(event, args, text)

    return False










from core import on, Event
from typing import Optional, Union, List
from plugins.message_content_tools import plaintext_if_prefix, remove_all_xml, remove_first_prefix
from plugins.auth import is_admin
from plugins.logger import log


class MC:
    def __init__(self, event: Event, args: list, text: str):
        self.event: Event = event
        self.args: list = args
        self.text: str = text

    def send(self, content: str):
        return self.event.message_create(content=content)


def match_command(event,
                  command: Optional[Union[List[str], str]] = None,
                  gap_less: bool = False, arg_less: bool = False,
                  admin_only: bool = False,
                  match_args: Optional[Union[List[str], str]] = None,
                  match_text: str = None) -> Optional[MC]:
    '''
    匹配命令

    Parameters:
    command (Optional[Union[List[str], str]]): 命令头，可以是list或者str
    gap_less (bool): 是否可以在命令头后不加空格
    arg_less (bool): 是否是无参数命令
    admin_only (bool): 是否只有管理员可以使用
    match_args (Optional[Union[List[str], str]]): 匹配参数列表，可以是list或者str
    match_text (str): 匹配参数文本

    Returns:
    Optional[MC]: 如果匹配到了，返回MC对象，否则返回None

    注意：
    必须要命令前缀匹配，才会触发。但如果你的命令前缀有''空字符串，任何消息都会触发。

    '''
    def match_args_(args: list, match_args: list) -> bool:
        log('args: ' + str(args))
        for item in match_args:
            if item in args:
                return True
        log('用户输入的参数里 没有任何参数与预设匹配')
        return False

    def match_text_(text: str, match_text: str) -> bool:
        log('text: ' + str(text))
        if match_text in text:
            return True
        log('用户输入的文本里 没有任何文本与预设匹配')
        return False

    def is_admin_(event: Event) -> bool:
        if is_admin(event.platform, event.user.id):
            return True
        log('用户不是管理员')
        return False

    def if_at_is_bot_(pure_msg: str) -> bool:
        if f'<at id="{event.self_id}' not in pure_msg and ('<at id="' in pure_msg and '"/>' in pure_msg):
            log('用户at了，但不是bot')
            return False
        return True

    if admin_only:
        if not is_admin_(event):
            return None

    if command is None:
        log('command is None')
        return MC(event, [], event.message.content)

    pure_msg = event.message.content

    if not if_at_is_bot_(pure_msg):
        return None

    pure_msg = plaintext_if_prefix(pure_msg).strip()

    if pure_msg == '':
        log('pure_msg is empty')
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
            log('不匹配 [' + item + '] 与 [' + pure_msg + ']')
            continue
        log('匹配到命令头了！！！！！')
        if match_args:
            log('存在match_args')
            if match_args_(args, match_args):
                return MC(event, args, text)
            else:
                log('虽然匹配了命令头，但是没有匹配到参数')
                if not match_text:  #`如果没有match_text，就不继续匹配了
                    continue

        if match_text:
            log('存在match_text')
            if match_text_(text, match_text):
                return MC(event, args, text)
            else:
                log('虽然匹配了命令头，但是没有匹配到文本')
                # 这是最后一项，如果没有匹配到，就直接continue
                continue

        log('匹配到命令')
        return MC(event, args, text)

    log('没有匹配到任何命令')
    return False










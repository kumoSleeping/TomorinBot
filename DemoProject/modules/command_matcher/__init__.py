from core import on, Event
from typing import Optional, Union, List

from modules.text_utils import plaintext_if_prefix, remove_all_xml, remove_first_prefix
from modules.logger import log
from modules.uni_manager import is_admin


class MC:
    def __init__(self, event: Event, args: list, text: str):
        '''
        匹配命令的对象
        entity of matching command

        :param event: Event 事件对象
        :param args: list 参数列表
        :param text: str 文本
        '''
        self.event: Event = event
        self.args: list = args
        self.text: str = text

    def send(self, content: str):
        return self.event.message_create(content=content)


def match_command(event: Event,
                  command: Optional[Union[List[str], str]] = None,
                  gap_less: bool = False, arg_less: bool = False,
                  admin_only: bool = False,
                  match_args: Optional[Union[List[str], str]] = None,
                  match_text: str = None) -> Optional[MC]:
    '''
    必须参数:
    event 对象  事件对象。
    command  指令头。

    可选参数:
    gap_less  如果为True，指令头不需要空格。
    arg_less  如果为True，指令头后面不能有参数。
    admin_only  如果为True，只有管理员才能触发。（管理员在配置文件里设置）
    match_args  如果有值，只有匹配到了这些参数才会触发。
    match_text  如果有值，只有匹配到了这些文本才会触发，与match_args有一个匹配即可。

    返回:
    Optional[MC] / None  如果匹配到了，返回一个"MC对象"，否则返回None。

    MC对象内含有三个属性：
    event: Event  事件对象本身。
    args: list  指令的参数列表 (不包括指令头)。
    text: str  指令的参数的文本 (去除了指令头的文本)。

    注意：
    必须要命令前缀匹配，才会触发。但如果你的命令前缀有''空字符串，任何消息都会触发。
    命令前缀在配置文件里设置。


    Required parameters:
    event object  Event object.
    command  Command header.

    Optional parameters:
    gap_less  If True, the command header does not need a space.
    arg_less  If True, there can be no parameters after the command header.
    admin_only  If True, only administrators can trigger.(Administrator is set in the configuration file)
    match_args  If there is a value, only if these parameters are matched will it be triggered.
    match_text  If there is a value, only if these texts are matched will it be triggered, either match_args or match_text is matched.

    Return:
    Optional[MC] / None  If matched, return a "MC object", otherwise return None.

    The MC object contains three attributes:
    event: Event  The event object itself.
    args: list  The list of command parameters (excluding the command header).
    text: str  The text of the command parameters (the text of the command header is removed).

    Note:
    Must match the command prefix to trigger. But if your command prefix is an empty string, any message will trigger.
    The command prefix is set in the configuration file.
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










from mods import on, Event
from typing import Optional, Union, List

from .text_utils import plaintext_if_prefix, remove_all_xml, remove_first_prefix
from .text_utils import log
from mods import is_admin


# seq = 1


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
        # global seq
        # # seq 自增
        # seq += 1
        # log.debug('seq: ' + str(seq))
        # msg = content + f'<passive id="{self.event.message.id}" seq="{seq}"/>'
        return self.event.message_create(content=content)


def match_command(event: Event,
                  commands: Optional[Union[List[str], str]] = '',
                  limit_arg_less: bool = False,
                  limit_admin: bool = False,
                  limit_at: bool = False,
                  allow_gap_less: bool = False,
                  allow_any_at: bool = False,
                  allow_quote: bool = False,
                  ) -> Optional[MC]:
    '''
    必须参数:
    event 对象  事件对象。
    commandss  指令头。

    可选参数:
    limit_arg_less  限制指令头后面不能有参数。
    limit_admin  限制只有管理员才能触发。（管理员在配置文件里设置）
    limit_at  限制at了bot才能触发，使用前确保你收到的消息里的at是完整正确的。
    allow_gap_less  容许指令头后不加空格。
    allow_any_at  容许存在at但是不是at的bot也会触发。(默认存在at但是不是at的bot不会触发)
    allow_quote  如果为True，存在引用消息才能触发。(默认存在引用消息就不会触发)

    返回:
    Optional[MC] / None  如果匹配到了，返回一个"MC 对象"，否则返回None。

    MC对象内含有三个属性：
    event: Event  事件对象本身。
    args: list  指令的参数列表 (不包括指令头)。
    text: str  指令的参数的文本 (去除了指令头的文本)。

    注意：
    必须要命令前缀匹配，才会触发。但如果你的命令前缀有''空字符串，任何消息都会触发。
    命令前缀在配置文件里设置。
    '''

    # 如果是管理员限定，但是不是管理员，就不会触发
    if limit_admin:
        if not is_admin(event.platform, event.user.id):
            return None

    pure_msg = event.message.content

    if not allow_any_at:
        # 如果存在at元素，但是不是at的bot，就不会触发
        if f'<at id="{event.self_id}' not in pure_msg and ('<at id="' in pure_msg and '"/>' in pure_msg):
            return None

    if not allow_quote:
        if '<quote' in pure_msg and '"/>' in pure_msg:
            return None

    if limit_at:
        # 如果没有at自己，就不会触发
        if f'<at id="{event.self_id}' and '"/>' not in pure_msg:
            return None

    pure_msg = plaintext_if_prefix(pure_msg).strip()

    log.debug('pure_msg: ' + pure_msg)

    # 统一处理为列表
    if isinstance(commands, str):
        command_list: list = [commands]
    elif isinstance(commands, list):
        command_list = commands
    else:
        return None

    for item in command_list:
        log.debug('item: ' + item)
        # 如果命令为空，就会理解为任何消息都会触发
        if item == '':
            log.debug('command is empty')
            return MC(event, [], pure_msg)

        # 从此处开始，下方四个分支只会有一个会被触发
        # 先匹配带空格的，剩下的再匹配不带空格的
        if pure_msg.startswith(item + ' ') and not limit_arg_less:
            args = pure_msg.split()[1:]
            text = pure_msg.replace(item + ' ', '', 1)
            return MC(event, args, text)

        # gap_less：容许不加空格
        elif allow_gap_less and pure_msg.startswith(item) and not limit_arg_less:
            args = pure_msg.split()[1:]
            text = pure_msg.replace(item, '', 1)
            return MC(event, args, text)

        # 完全匹配
        elif pure_msg == item:
            args = []
            text = ''
            return MC(event, args, text)

    else:
        return None











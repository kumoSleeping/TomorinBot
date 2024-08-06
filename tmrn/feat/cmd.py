from typing import List, Optional, Union
from satori.client import Event


def cmd_select(
        event: Event,
        prefix: Union[str, List[str]] = '',
        white_user: Union[Optional[str], List[str]] = None,
        ) -> Optional[str]:
    '''
    # 用于在在合适的时候获取适合于命令的纯文本信息
    > 本身不包含命令处理

    - 当发消息者是自身时，返回 None
    - 当消息中有 at 时，如果at的是bot，返回 pure_text，否则返回 None
    - 当消息中有引用时，如果引用的是bot，返回 pure_text，否则返回 None
    - 当 prefix 被规定时，如果消息以 prefix 开头，返回 pure_text，否则返回 None，如果是 '' 空字符串，任何消息都会触发
    - 如果 white_user 被规定时，消息发送者在 white_user 中才会触发，否则不会触发
    '''
    msg = event.message.message
    pure_text = ''.join(str(e) for e in msg if e.tag == 'text').strip()

    if white_user:
        if isinstance(white_user, str):
            white_user = [white_user]
        for user in white_user:
            if user == event.user.id:
                break
        else:
            return

    if event.user.id == event.self_id:
        return

    if pure_text == '':
        return
    for e in msg:
        if e.tag == 'at':
            if e['id'] == event.self_id:
                # e 大循环 continue 进入下一个循环
                continue
            return
        elif e.tag == 'quote':
            if e._children:
                for child_e in e._children:
                    if child_e.tag == 'author' and child_e['id'] == event.self_id:
                        break
                else:
                    return None
            else:
                # 没有子元素，返回 None
                return None
    if prefix != ['']:
        prefix = prefix if isinstance(prefix, list) else [prefix]
        for p in prefix:
            if p == '' or pure_text.startswith(p):
                return pure_text[len(p):].strip()
    else:
        return pure_text
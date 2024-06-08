from satori.client import WebsocketsInfo, EventType, Account, Event
from satori.model import LoginStatus
from satori.event import MessageEvent, LoginEvent
from satori.element import Element, E, Message
from typing import List, Union, Optional

from tmrn.log import log, c

import asyncio
from contextvars import ContextVar

from tmrn.start import app


@app.lifecycle
async def login_disp(account: Account, event: LoginStatus):
    if event == 2:
        res = await account.login_get()
        name = res.user.name
        if name == '':
            name = 'NO-NAME-BOT'
        status = res.status
        platform = res.platform
        if status == 1:
            log.success(
                f"linked {c.bright_red}Satori Driver{c.reset} {c.bright_yellow}{c.style.bold}{c.style.underline}{name}{c.reset} login {c.bright_green}{platform}{c.reset}.")
        else:
            log.warning(
                f"linked {c.bright_red}Satori Driver{c.reset} {c.bright_yellow}{c.style.bold}{c.style.underline}{name}{c.reset} sleep in {c.bright_green}{platform}{c.reset}.")
    elif event == 1:
        log.info(f"linkin' {c.bright_red}Satori Driver{c.reset}...")

    elif event == 0:
        log.info(f"linkin' {c.bright_red}Satori Driver{c.reset} {c.bright_red}offline{c.reset}.")


@app.register
async def meg_disp(account: Account, event: MessageEvent):
    def log_msg(message: List[Element]):
        new_msg = ''
        for item in message:
            if item.tag == 'text':
                new_msg += str(item)
            elif item.tag == 'at':
                new_msg += f'{c.bright_yellow}@{item["name"]}{c.reset}' if item[
                    'name'] else f'{c.bright_yellow}@{item["id"]}{c.reset}'
            elif item.tag == 'quote':
                new_msg += f'{c.style.bold}{c.style.underline}{c.blue}[{item.tag} {c.reset}'

                if item._children:

                    for child_item in item._children:
                        if child_item.tag == 'author':
                            new_msg += f'{c.style.underline}{c.bright_yellow}{child_item["name"]}: {c.reset}'
                        elif child_item.tag == 'text':
                            new_msg += f'{c.style.underline}{child_item}{c.reset}'
                        else:
                            new_msg += f'{c.style.underline}{c.blue}[{child_item.tag}]{c.reset}'
                new_msg += f'{c.style.underline}{c.style.bold}{c.blue}]{c.reset} '
            else:
                new_msg += f'{c.style.bold}{c.blue}[{item.tag}]{c.reset}'
        # print(new_msg)
        # 将所有HTML标签替换为占位符
        count_msg = new_msg.replace(f'{c.blue}', '').replace(f'{c.reset}', '').replace(f'{c.bright_yellow}', '')
        # print(count_msg)
        cleaned_text = new_msg[0:100] + f'...{c.reset}' if len(count_msg) > 100 else new_msg
        cleaned_text = cleaned_text.replace("\n", " ").replace("\r", " ")
        return cleaned_text

    try:
        if event.type == 'internal':
            log.info(f"<{event.platform}> | {event.type}:{event._type}")
            return

        # 处理可能为None的字段
        user_name = event.user.name if event.user.name else "Unknown"
        guild_name = event.guild.name if event.guild.name else "Unknown"
        channel_name = event.channel.name if event.channel.name else "Unknown"

        # 构建用户、频道和服务器信息
        user = f"{user_name}<{event.user.id}>"
        guild = f"{guild_name}<{event.guild.id}>"
        channel = f"{channel_name}<{event.channel.id}>"
        place = f"{guild} -> {channel}" if channel_name != guild_name else channel

        if event.type != 'message-created':
            log.info(
                f"{c.bright_magenta}{event.type}{c.reset} {c.bright_green}{event.platform}{c.reset}:{c.bright_blue}{place}{c.reset} | {c.bright_yellow}{user}{c.reset}")

        elif event.type == 'message-created':
            cleaned_text = log_msg(event.message.message)
            log.info(
                f"{c.bright_magenta}{event.type}{c.reset} {c.bright_green}{event.platform}{c.reset}:{c.bright_blue}{place}{c.reset} | {c.bright_yellow}{user}{c.reset}: {cleaned_text}")
    except Exception as e:
        log.error(f'无法显示日志 {e}')
    return event


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
                # 遍历每个子元素
                for child_e in e._children:
                    if child_e.tag == 'author' and child_e['id'] == event.self_id:
                        # 找到匹配项，跳出子循环，并继续外层循环
                        break
                else:
                    # 如果子循环完整执行（未通过 break 跳出），则返回 None
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


union_user_channel = ContextVar("union_user_channel", default={})


@app.register_on(EventType.MESSAGE_CREATED)
async def union_user_channel_enqueue_response(account: Account, event: Event):
    queue_key = (event.self_id, event.channel.id, event.user.id)
    queues = union_user_channel.get()
    if queue_key in queues:
        await queues[queue_key].put(event)


async def sub_input(event: Event, timeout: int = 60) -> Optional[Event]:
    self_id = event.self_id
    channel_id = event.channel.id
    user_id = event.user.id
    queues = union_user_channel.get()
    queue_key = (self_id, channel_id, user_id)

    if queue_key not in queues:
        queues[queue_key] = asyncio.Queue()
        union_user_channel.set(queues)

    try:
        response = await asyncio.wait_for(queues[queue_key].get(), timeout)
        # 删除队列以释放资源
        del queues[queue_key]
        union_user_channel.set(queues)
        return response
    except asyncio.TimeoutError:
        # 在超时后也应该清理队列
        del queues[queue_key]
        union_user_channel.set(queues)
        return None
    finally:
        # 无论是否超时，都应该清理队列
        if queue_key in queues:
            del queues[queue_key]
            union_user_channel.set(queues)


channel = ContextVar("channel", default={})


@app.register_on(EventType.MESSAGE_CREATED)
async def channel_enqueue_response(account: Account, event: Event):
    channel_key = (event.self_id, event.channel.id)
    queues = channel.get()
    if channel_key in queues:
        await queues[channel_key].put(event)


async def sub_channel_input(event: Event, timeout: int = 60) -> Optional[Event]:
    self_id = event.self_id
    channel_id = event.channel.id
    queues = channel.get()
    channel_key = (self_id, channel_id)

    if channel_key not in queues:
        queues[channel_key] = asyncio.Queue()
        channel.set(queues)

    try:
        response = await asyncio.wait_for(queues[channel_key].get(), timeout)
        # 删除队列以释放资源
        del queues[channel_key]
        channel.set(queues)
        return response
    except asyncio.TimeoutError:
        # 在超时后也应该清理队列
        del queues[channel_key]
        channel.set(queues)
        return None
    finally:
        # 无论是否超时，都应该清理队列
        if channel_key in queues:
            del queues[channel_key]
            channel.set(queues)


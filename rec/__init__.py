import re
from core.interfaces import config, on, Event, log, c
from satori import Element, E
from typing import List, Union


@on.bot_api_requested
async def display_send_async(event: Event, method: str, data: dict, platform: str, self_id: str, response):
    try:
        log.info(f'{c.bright_magenta}{method}{c.reset} -> {c.bright_green}{platform}{c.reset}')
    except Exception as e:
        if not response:
            log.error(f'无法显示日志 {e}')
        else:
            log.error(f'无法显示日志 {e} {response.text}')


@on.bot_event_built
async def display_receive(event: Event):
    def log_msg(message: List[Element]):
        new_msg = ''
        for item in message:
            if item.tag == 'text':
                new_msg += str(item)
            elif item.tag == 'at':
                new_msg += f'{c.bright_yellow}@{item["name"]}{c.reset}' if item['name'] else f'{c.bright_yellow}@{item["id"]}{c.reset}'
            elif item.tag == 'quote':
                new_msg += f'{c.style.bold}{c.style.underline}{c.blue}[{item.tag} {c.reset}'

                if item._children:

                    for chlid_item in item._children:
                        if chlid_item.tag == 'author':
                            new_msg += f'{c.style.underline}{c.bright_yellow}{chlid_item["name"]}: {c.reset}'
                        elif chlid_item.tag == 'text':
                            new_msg += f'{c.style.underline}{chlid_item}{c.reset}'
                        else:
                            new_msg += f'{c.style.underline}{c.blue}[{chlid_item.tag}]{c.reset}'
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




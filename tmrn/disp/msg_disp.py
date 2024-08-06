from typing import List
from tmrn import c, log, app
from satori.client import Account
from satori.element import Element
from satori.event import MessageEvent


@app.register
async def msg_disp(account: Account, event: MessageEvent):
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

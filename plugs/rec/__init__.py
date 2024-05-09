from requests import Response
from mods import config, on, Event

from mods import easy_to_show_text, log, c


@on.bot_event_built
def display_receive(event: Event):
    try:
        show_event_log(event)
    except Exception as e:
        log.error(f'无法显示日志 {e}')
    return event


@on.bot_api_requested
def display_send(event: Event, method: str, data: dict, platform: str, self_id: str, response: Response):
    try:
        log.info(f'{c.bright_magenta}{method}{c.reset} -> {c.bright_green}{platform}{c.reset}')
    except Exception as e:
        if not response:
            log.error(f'无法显示日志 {e}')
        else:
            log.error(f'无法显示日志 {e} {response.text}')
    return event, method, data, platform, self_id, response


def show_event_log(event):
    if event.type == 'internal':
        log.info(f"<{event.platform}> | {event.type}:{event._type}")
        return
    # 展示日志
    cleaned_text = easy_to_show_text(event.message.content)

    user = event.user.name + f'<{event.user.id}>'
    guild = event.guild.name + f'<{event.guild.id}>'
    channel = event.channel.name + f'<{event.channel.id}>'
    place = channel if channel == guild else guild + '->' + channel
    # 获取24小时制度当前时间

    if event.type != 'internal':
        log.info(f"{c.bright_magenta}{event.type}{c.reset} {c.bright_green}{event.platform}{c.reset}:{c.bright_blue}{place}{c.reset} | {c.bright_yellow}{user}{c.reset}: {cleaned_text}")




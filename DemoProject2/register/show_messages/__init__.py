import re
import json
from datetime import datetime
import time
from requests import Response
from core import config, on, Event

from modules import easy_to_show_text


@on.after_event
def display_receive(event: Event):
    # print(event.message.content)
    try:
        show_event_log(event)
    except Exception as e:
        print(f'[display_logs] 无法显示日志', e)
    return event


@on.after_request
def display_send(event: Event, method: str, data: dict, platform: str, self_id: str, response: Response):
    try:
        print(f'\033[37m  [send] {method} -> {platform} {data.get("message_id", "")} \033[0m')
    except Exception as e:
        if not response:
            print(f'[display_logs] 无法显示日志: 返回值为空')
        else:
            print(f'[display_logs] 无法显示日志 {e}')
    return event, method, data, platform, self_id, response


def show_event_log(event):
    msg_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')

    if event.type == 'internal':
        print(f"\033[37m  [display_logs] | {msg_time} | [ {event.platform} ] < {event.type} > [{event._type}]\033[0m")
        return
    # 展示日志
    cleaned_text = easy_to_show_text(event.message.content)

    user = event.user.name + f'<{event.user.id}>'
    guild = event.guild.name + f'<{event.guild.id}>'
    channel = event.channel.name + f'<{event.channel.id}>'
    place = channel if channel == guild else guild + '->' + channel
    # 获取24小时制度当前时间

    if event.type != 'internal':
        print(f"\033[37m  [display_logs] | {msg_time} | [ {event.platform}: {place} ] < {event.type} >（ {user} ）{cleaned_text}\033[0m")




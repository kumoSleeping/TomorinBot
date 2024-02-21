from core import on, Event

from requests import Response


@on.after_request
def display_send(event: Event, method: str, data: dict, platform: str, self_id: str, response: Response):
    '''
    发送消息后提示
    '''
    try:
        print(f'\033[37m  [send] {method} -> {platform} {data.get("message_id", "")}  \033[0m')
    except Exception as e:
        pass
    return event, method, data, platform, self_id, response


@on.after_event
def display_receive(event: Event):
    '''
    接收到消息后提示
    '''
    try:
        print(f'\033[37m  [receive] {event.platform} {event.type} {event.message.content}  \033[0m')
    except Exception as e:
        print(f'[display_logs] 无法显示日志', e)
    return event


@on.message_created
def echo(event: Event):
    '''
    实现echo功能
    '''
    # print(event.message.content)
    if event.message.content.startswith('echo '):
        event.message_create(event.message.content[5:])
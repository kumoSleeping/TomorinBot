from modules import interval_do, auto_asset_path
from core import on, Event
from modules import save_send_message, save_receive_message, delete_old_records, EventReceive, EventSend
from requests import Response

@interval_do(1*60*60)
def delete_old_records_():
    """ 删除过期的记录 """
    delete_old_records(EventReceive, 24)
    delete_old_records(EventSend, 24)


delete_old_records_()


@on.after_request
def save_send(event: Event, method: str, data: dict, platform: str, self_id: str, response: Response):
    """ 保存发送的消息 """
    try:
        save_send_message(data.get('content'), data.get('channel_id'), self_id)
    except:
        print(f'[Transceiver analysis] 无法保存发送的消息')
    return event, method, data, platform, self_id, response


@on.after_event
def save_receive(event: Event):
    """ 保存接收到的消息 """
    try:
        save_receive_message(event.type, event.message.content, event.user.id, event.channel.id)
    except:
        print(f'[Transceiver analysis] 无法保存接收到的消息')
    return event




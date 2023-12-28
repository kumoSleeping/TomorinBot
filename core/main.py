import threading

from core.event import Event
from core.loader import loaded_func
from core.loader import before_event, before_plugin_do, after_event


function_info_list = []


def main(data):
    if before_event:
        for k, v in before_event.items():
            data = v(data)
    event = Event(data)
    if after_event:
        for k, v in after_event.items():
            event = v(event)
    for k, v in loaded_func.items():
        # before_plugin_do
        if before_plugin_do:
            for k2, v2 in before_plugin_do.items():
                event, v = v2(event, v)
        if data['type'] == 'internal':
            plugin_thread = threading.Thread(target=v, args=(event,))
            plugin_thread.start()
        else:
            # 使用 session 的副本创建并启动插件线程
            plugin_thread = threading.Thread(target=v, args=(event,))
            plugin_thread.start()







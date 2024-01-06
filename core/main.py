import threading

from core.event import Event
from core.loader import loaded_func
from core.loader import before_event, before_plugin_do, after_event
import gc


function_info_list = []


def main(data):

    if before_event:
        for i_1 in before_event:
            data = i_1(data)
    if not data:
        return

    event = Event(data)

    if after_event:
        for i_2 in after_event:
            event = i_2(event)
    if not event:
        return

    for i_3 in loaded_func:

        if before_plugin_do:
            for i_4 in before_plugin_do:
                event, i_3 = i_4(event, i_3)
        if not event:
            return

        if data['type'] == 'internal':
            plugin_thread = threading.Thread(target=i_3, args=(event,))
            plugin_thread.start()
        else:
            # 使用 session 的副本创建并启动插件线程
            plugin_thread = threading.Thread(target=i_3, args=(event,))
            plugin_thread.start()
    # 释放资源
    gc.collect()







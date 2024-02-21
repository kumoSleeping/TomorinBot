import threading

from core.event import Event
from core.loader import plugin_manager
import gc


function_info_list = []


def main(data):

    if plugin_manager.before_event:
        for before_event_item in plugin_manager.before_event:
            data = before_event_item(data)
            if not data:
                return

    event = Event(data)

    if plugin_manager.after_event:
        for after_event_item in plugin_manager.after_event:
            event = after_event_item(event)
            if not event:
                return

    for loaded_func_item in plugin_manager.loaded_func:

        if plugin_manager.before_plugin_do:
            for before_plugin_do_item in plugin_manager.before_plugin_do:
                event, _ = before_plugin_do_item(event, loaded_func_item)
                if not event:
                    return

        plugin_thread = threading.Thread(target=loaded_func_item, args=(event,))
        plugin_thread.start()

    # 释放资源
    gc.collect()


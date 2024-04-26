import threading

from core.event import Event
from core.config import registers_manager
from core.log import log
import gc


function_info_list = []


def msg_push(data):
    try:
        if registers_manager.before_api_request_tag:
            for before_event_item in registers_manager.before_data_to_event_tag:
                data = before_event_item(data)
                # 确保返回值符合预期，否则跳过当前循环或执行其他操作
                if not isinstance(data, (dict, list, str)):  # 根据实际需要调整期望的类型
                    log.error("An error occurred, perhaps <on.before_api_request> returned value count is not correct.")
                    return

        event = Event(data)

        if registers_manager.after_data_to_event_tag:
            for after_event_item in registers_manager.after_data_to_event_tag:
                event = after_event_item(event)
                # 同样确保返回值符合预期
                if not isinstance(event, Event):  # 确保event是Event类型的实例
                    log.error("An error occurred, perhaps <on.after_data_to_event> returned value count is not correct.")
                    return

        for loaded_func_item in registers_manager.standard_event_tag:

            if registers_manager.before_data_to_event_tag:
                for before_plugin_do_item in registers_manager.before_data_to_event_tag:
                    event, _ = before_plugin_do_item(event, loaded_func_item)
                    # 验证event的类型，防止错误
                    if not isinstance(event, Event):
                        log.error("An error occurred, perhaps <on.before_plugin_do> returned value count is not correct.")
                        return

            plugin_thread = threading.Thread(target=loaded_func_item, args=(event,))
            plugin_thread.start()

    except Exception as e:
        log.error('Error occurred.')
        raise e

    finally:
        # 无论如何都会执行的清理代码
        gc.collect()



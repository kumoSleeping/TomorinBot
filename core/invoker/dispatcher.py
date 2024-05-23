import threading
import inspect
import gc
from core.classes.log import log

from core.classes.event import Event, EventAsync, EventInternal
from __main__ import initialize_manager


async def build_session_async(data):
    try:
        if data.get('type') == 'internal':
            event = EventInternal(data['data'])
        else:
            event = EventAsync(data)

        if initialize_manager._event_built:
            for after_event_item in initialize_manager._event_built:
                if event:
                    if inspect.iscoroutinefunction(after_event_item):
                        await after_event_item(event)
        for loaded_func_item in initialize_manager._satori_event:
            if initialize_manager._satori_event:
                if inspect.iscoroutinefunction(loaded_func_item):
                    await loaded_func_item(event)
    except Exception as e:
        log.error('Error occurred.')
        raise e
    finally:
        gc.collect()


def build_session_sync(data: dict):
    try:
        if data.get('type') == 'internal':
            event = EventInternal(data['data'])
        else:
            event = Event(data)

        if initialize_manager._event_built:
            for after_event_item in initialize_manager._event_built:
                if event:
                    if not inspect.iscoroutinefunction(after_event_item):
                        threading.Thread(target=after_event_item, args=(event,)).start()
        for loaded_func_item in initialize_manager._satori_event:
            if initialize_manager._satori_event:
                if not inspect.iscoroutinefunction(loaded_func_item):
                    threading.Thread(target=loaded_func_item, args=(event,)).start()

    except Exception as e:
        log.error('Error occurred.')
        raise e

    finally:
        # 无论如何都会执行的清理代码
        gc.collect()

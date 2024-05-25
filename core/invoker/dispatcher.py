import threading
import inspect
import gc
import asyncio

from core.classes.log import log
from core.classes.event import Event
from core.classes.event_nonstandard import EventNonstandard

from __main__ import initialize_manager, config


async def parse_event(data: dict):
    try:
        event = Event.parse(data)
    except Exception as e:
        log.warning(f'Event parse error, try parse EventNonstandard. data: {data}')
        try:
            event = EventNonstandard(data)
        except Exception as e:
            log.error(f'Error occurred, data: {data}')
            raise e
    if config.get_key('support_async'):
        threading.Thread(target=build_session_sync, args=(event,)).start()
    await build_session_async(event)


async def build_session_async(event: Event):
    try:
        if initialize_manager._event_built:
            for after_event_item in initialize_manager._event_built:
                if event and inspect.iscoroutinefunction(after_event_item):
                    task = asyncio.create_task(after_event_item(event))

        if initialize_manager._satori_event:
            for loaded_func_item in initialize_manager._satori_event:
                if inspect.iscoroutinefunction(loaded_func_item):
                    task = asyncio.create_task(loaded_func_item(event))

    except Exception as e:
        log.error('Error occurred.')
        raise e
    finally:
        gc.collect()


def build_session_sync(event: Event):
    try:
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

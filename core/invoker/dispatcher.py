import threading
import inspect
import gc
import asyncio

from core.classes.log import log
from core.classes.event import Event
from core.classes.event_nonstandard import EventNonstandard

from __main__ import initialize_manager


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
    task = asyncio.create_task(build_session(event))


async def build_session(event: Event):
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



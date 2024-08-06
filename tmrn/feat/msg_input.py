import asyncio
from contextvars import ContextVar
from tmrn.start import app
from satori.client import Account, Event, EventType
from typing import Optional


union_user_channel = ContextVar("union_user_channel", default={})


@app.register_on(EventType.MESSAGE_CREATED)
async def union_user_channel_enqueue_response(account: Account, event: Event):
    queue_key = (event.self_id, event.channel.id, event.user.id)
    queues = union_user_channel.get()
    if queue_key in queues:
        await queues[queue_key].put(event)


async def sub_input(event: Event, timeout: int = 60) -> Optional[Event]:
    self_id = event.self_id
    channel_id = event.channel.id
    user_id = event.user.id
    queues = union_user_channel.get()
    queue_key = (self_id, channel_id, user_id)

    if queue_key not in queues:
        queues[queue_key] = asyncio.Queue()
        union_user_channel.set(queues)

    try:
        response = await asyncio.wait_for(queues[queue_key].get(), timeout)
        # 删除队列以释放资源
        del queues[queue_key]
        union_user_channel.set(queues)
        return response
    except asyncio.TimeoutError:
        # 在超时后也应该清理队列
        del queues[queue_key]
        union_user_channel.set(queues)
        return None
    finally:
        # 无论是否超时，都应该清理队列
        if queue_key in queues:
            del queues[queue_key]
            union_user_channel.set(queues)


channel = ContextVar("channel", default={})


@app.register_on(EventType.MESSAGE_CREATED)
async def channel_enqueue_response(account: Account, event: Event):
    channel_key = (event.self_id, event.channel.id)
    queues = channel.get()
    if channel_key in queues:
        await queues[channel_key].put(event)


async def sub_channel_input(event: Event, timeout: int = 60) -> Optional[Event]:
    self_id = event.self_id
    channel_id = event.channel.id
    queues = channel.get()
    channel_key = (self_id, channel_id)

    if channel_key not in queues:
        queues[channel_key] = asyncio.Queue()
        channel.set(queues)

    try:
        response = await asyncio.wait_for(queues[channel_key].get(), timeout)
        # 删除队列以释放资源
        del queues[channel_key]
        channel.set(queues)
        return response
    except asyncio.TimeoutError:
        # 在超时后也应该清理队列
        del queues[channel_key]
        channel.set(queues)
        return None
    finally:
        # 无论是否超时，都应该清理队列
        if channel_key in queues:
            del queues[channel_key]
            channel.set(queues)


import aiohttp
import asyncio
import inspect

from core.__main__ import config
from core.classes.log import log

from __main__ import initialize_manager


async def async_request_by_aiohttp(event, data: dict, headers: dict, full_address: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(full_address, json=data, headers=headers) as response:
                response.raise_for_status()
                json_response = await response.json()
        return event, data, headers, full_address, json_response
    except aiohttp.ClientResponseError as exc:
        log.error(f"请求失败，状态码：{exc.status}, 响应：{exc.message}")
        raise
    except Exception as exc:
        log.error(f"请求错误：{str(exc)}")
        raise


def call_api(event, method: str, data: dict, platform: str, self_id: str, internal=False):
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            return call_api_async(event, method, data, platform, self_id, internal)
    except RuntimeError:
        # 没有运行中的事件循环，使用同步函数
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(call_api_async(event, method, data, platform, self_id, internal))


async def call_api_async(event, method: str, data: dict, platform: str, self_id: str, internal=False):
    connection = find_connection(self_id)
    if connection is None:
        return None

    full_address = build_full_address(connection, method, internal)
    headers = build_headers(connection, platform, self_id)

    response_dict = await async_request_by_aiohttp(event, data, headers, full_address)
    if initialize_manager._api_requested:
        for item in initialize_manager._api_requested:
            if inspect.iscoroutinefunction(item):
                await item(event, method, data, platform, self_id, response_dict)
    return response_dict


def find_connection(self_id):
    for connection in config.get_key('websocket_connections'):
        if self_id in connection["self_ids"]:
            return connection
    log.error(f'未找到匹配的连接配置，self_id：{self_id}')
    return None


def build_full_address(connection, method, internal):
    address = connection['address']
    http_protocol = connection.get('http_protocol', 'http')
    api_segment = 'v1/internal' if internal else 'v1'
    return f'{http_protocol}://{address}/{api_segment}/{method}'


def build_headers(connection, platform, self_id):
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {connection["token"]}',
        'X-Platform': platform,
        'X-Self-ID': self_id
    }




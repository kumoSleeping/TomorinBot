import aiohttp
import asyncio
import inspect
import threading
import urllib.request
import urllib.error
import json

from core.__main__ import config
from core.classes.log import log

from __main__ import initialize_manager


def sync_request_by_urllib(event, data: dict, headers: dict, full_address: str):
    try:
        data_bytes = json.dumps(data).encode('utf-8')  # 编码 JSON 数据
        req = urllib.request.Request(full_address, data=data_bytes, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            response_data = response.read()
            json_response = json.loads(response_data.decode('utf-8'))
            if response.status != 200:
                raise urllib.error.HTTPError(full_address, response.status, "HTTP request failed", response.getheaders(), None)
        return event, data, headers, full_address, json_response
    except urllib.error.HTTPError as exc:
        log.error(f"请求失败，状态码：{exc.code}, 响应：{exc.read().decode('utf-8')}")
        raise
    except Exception as exc:
        log.error(f"请求错误：{str(exc)}")
        raise


async def async_request_by_aiohttp(event, data: dict, headers: dict, full_address: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(full_address, json=data, headers=headers) as response:
                response.raise_for_status()
                json_response = await response.json()
        return event, data, headers, full_address, json_response
    except aiohttp.ClientResponseError as exc:
        log.error(f"请求失败，状态码：{exc.status}, 响应：{await exc.response.text()}")
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
        return call_api_sync(event, method, data, platform, self_id, internal)


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


def call_api_sync(event, method: str, data: dict, platform: str, self_id: str, internal=False):
    connection = find_connection(self_id)
    if connection is None:
        return None

    full_address = build_full_address(connection, method, internal)
    headers = build_headers(connection, platform, self_id)

    response_dict = sync_request_by_urllib(event, data, headers, full_address)
    if initialize_manager._api_requested:
        for item in initialize_manager._api_requested:
            if not inspect.iscoroutinefunction(item):
                threading.Thread(target=item, args=(event, method, data, platform, self_id, response_dict)).start()
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




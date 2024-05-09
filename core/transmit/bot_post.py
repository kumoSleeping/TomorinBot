from core.__main__ import config
from core.classes.utils import log

import requests
import json

from __main__ import initialize_manager


def request_by_requests(event, data: dict, headers: dict, full_address: str):
    response = requests.post(full_address, data=json.dumps(data), headers=headers, verify=True)
    # 检查响应
    if response.status_code == 200:
        try:
            # 解析响应为JSON格式
            response_data = response.json()
            rep_dict = response_data
            return event, data, headers, full_address, rep_dict
        except Exception:
            raise Exception(log.error(f'未能解析响应为JSON格式，响应：{response.text}'))
    else:
        # 抛出错误
        raise Exception(log.error(f'请求失败，状态码：{response.status_code}，响应：{response.text}'))


def api_request(event, method: str, data: dict, platform: str, self_id: str, internal=False):
    """
    发送消息到指定频道。

    Parameters:
    method (str): API方法。
    data (dict): 消息内容。
    platform (str): 平台名称。
    self_id (str): 平台账号。

    Returns:
    dict: 包含消息信息的字典，如果发送失败则返回None。
    """

    # 遍历连接配置
    for connection in config.get_key('websocket_connections'):
        if self_id in connection["self_ids"]:
            this_connection = connection
            break
    else:
        # 如果未找到匹配的连接配置
        log.error(f'未找到匹配的连接配置，self_id：{self_id}')
        return None

    # API endpoint
    address = this_connection['address']
    token = this_connection['token']
    http_protocol = this_connection.get('http_protocol', 'http')
    # 构建完整的API地址
    full_address = f'{http_protocol}://{address}/v1/{method}'
    if internal:
        full_address = f'{http_protocol}://{address}/v1/internal/{method}'

    # 构建请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'X-Platform': platform,
        'X-Self-ID': self_id
    }

    try:
        result = request_by_requests(event, data, headers, full_address)
        event, data, headers, full_address, response_dict = result
        # 调用after_request
        if initialize_manager._api_requested:
            for item in initialize_manager._api_requested:
                item(event, method, data, platform, self_id, response_dict)

    except Exception as e:
        log.error('Error occurred.')
        raise e

from core.config import registers_manager, config
from core.log import log

import requests
import json


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
            # raise Exception(f'[core] 未能解析响应为JSON格式，响应：{response.text}')
            raise Exception(log.error(f'未能解析响应为JSON格式，响应：{response.text}'))
    else:
        # 抛出错误
        raise Exception(log.error(f'请求失败，状态码：{response.status_code}，响应：{response.text}'))


def send_request(event, method: str, data: dict, platform: str, self_id: str, internal=False):
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
    for connection in config["core"]["websocket_connections"]:
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
    full_address = f'{http_protocol}://{address}/{method}'
    if internal:
        full_address = f'{http_protocol}://{address}/internal/{method}'

    # 构建请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'X-Platform': platform,
        'X-Self-ID': self_id
    }

    response_dict = {}

    try:
        # 调用before_request
        if registers_manager.before_request:
            for before_request_item in registers_manager.before_request:
                result = before_request_item(event, method, data, platform, self_id)
                # 验证返回值包含所有必要的元素
                if not isinstance(result, tuple) or len(result) != 5:
                    log.error("Perhaps returned value count is not correct.")
                    raise e
                event, method, data, platform, self_id = result

        # 发送POST请求
        response_dict = {}  # 假设存在此变量以便于示例编译通过
        result = request_by_requests(event, data, headers, full_address)
        # 验证返回值包含所有必要的元素
        if not isinstance(result, tuple) or len(result) != 5:
            log.error("Perhaps returned value count is not correct.")
            raise e
        event, data, headers, full_address, response_dict = result

        # 调用after_request
        if registers_manager.after_request:
            for after_request_item in registers_manager.after_request:
                result = after_request_item(event, method, data, platform, self_id, response_dict)
                # 验证返回值包含所有必要的元素
                if not isinstance(result, tuple) or len(result) != 6:
                    log.error("Perhaps returned value count is not correct.")
                    raise e
                event, method, data, platform, self_id, response_dict = result

    except Exception as e:
        log.error('Error occurred.')
        raise e

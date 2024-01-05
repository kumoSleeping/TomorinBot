from core.loader import config, before_request, after_request, satori_post


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
    # print(config)

    # 遍历连接配置
    for connection in config["websocket_client"]["connections"]:
        if self_id in connection["self_ids"]:
            this_connection = connection
            break
    else:
        # 如果未找到匹配的连接配置
        print(f"[core] 未找到 self_id 为 {self_id} 的连接配置")
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

    # 调用before_request
    if before_request:
        print(before_request)
        for i in before_request:
            event, method, data, platform, self_id = i(event, method, data, platform, self_id)
    # 发送POST请求
    if satori_post:
        for i in satori_post:
            event, data, headers, full_address, response_dict = i(event, data, headers, full_address)
            break  # 只取第一个
        # 调用after_request
        if after_request:
            for i in after_request:
                event, method, data, platform, self_id, response_dict = i(event, method, data, platform, self_id, response_dict)
    else:
        print(f"[core] [request] 未找到 satori_post 组件")




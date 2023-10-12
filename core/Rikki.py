import requests
import json
from server import TOKEN, IP, PORT


'''
Rikki.py · send
处理「satori」协议的信息发送 / API上报
'''


def send_message(message_content, platform, channel_id, self_id):
    """
    发送消息到指定频道。

    Parameters:
    channel_id (str): 频道ID。
    message_content (str): 消息内容。
    bearer_token (str): 认证Token。
    platform (str): 平台名称。
    self_id (str): 平台账号。

    Returns:
    dict: 包含消息信息的字典，如果发送失败则返回None。
    """
    # API endpoint

    endpoint = f'http://{IP}:{PORT}/v1/message.create'  # 替换为实际API endpoint

    # 构建请求参数
    request_data = {
        'channel_id': channel_id,
        'content': message_content
    }

    # 构建请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}',
        'X-Platform': platform,
        'X-Self-ID': self_id
    }

    # 发送POST请求
    # response = requests.post(endpoint, data=json.dumps(request_data), headers=headers)
    response = requests.post(endpoint, data=json.dumps(request_data), headers=headers, verify=True)

    # 检查响应
    if response.status_code == 200:
        # 解析响应为JSON格式
        response_data = response.json()
        return response_data
    else:
        print('Failed to create message. Status code:', response.status_code)
        return None


def send(message_content, session):
    send_message(message_content=message_content, platform=session.platform, channel_id=session.guild.id,
                 self_id=session.self_id)













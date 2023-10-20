import requests
import json

from core.Soyorin import TOKEN, IP, PORT

'''
Rikki.py · send
处理「satori」协议的信息发送 / API上报
'''


class Rikki:
    @staticmethod
    def send_request(method, data, platform, self_id):
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
        method = 'message.create'
        endpoint = f'http://{IP}:{PORT}/v1/{method}'  # 替换为实际API endpoint

        # 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {TOKEN}',
            'X-Platform': platform,
            'X-Self-ID': self_id
        }

        # 发送POST请求
        # response = requests.post(endpoint, data=json.dumps(request_data), headers=headers)
        response = requests.post(endpoint, data=json.dumps(data), headers=headers, verify=True)

        # 检查响应
        if response.status_code == 200:
            # 解析响应为JSON格式
            response_data = response.json()
            return response_data
        else:
            print('Status code:', response.status_code)
            return None


class Bot:
    @staticmethod
    def send(message_content, platform, channel_id, self_id):
        return Rikki.send_request(method='message.create', data={
                'channel_id': channel_id,
                'content': message_content
            }, platform=platform, self_id=self_id)

    @staticmethod
    def call_api(method, data, platform, self_id):
        return Rikki.send_request(method=method, data=data, platform=platform, self_id=self_id)


bot = Bot()






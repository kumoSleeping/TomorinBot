import requests
import json

from core import on, Event


@on.satori_post
def _satori_post(event: Event, data: dict, headers: dict, full_address: str):
    response = requests.post(full_address, data=json.dumps(data), headers=headers, verify=True)
    # 检查响应
    if response.status_code == 200:
        try:
            # 解析响应为JSON格式
            response_data = response.json()
            # print(response)
            rep_dict = response_data
            return event, data, headers, full_address, rep_dict
        except Exception:
            raise Exception(f'[core] 未能解析响应为JSON格式，响应：{response.text}')
    else:
        # 抛出错误
        raise Exception(f'[core] 发送消息失败，状态码：{response.status_code}，响应：{response.text}')


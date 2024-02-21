from core.loader import plugin_manager, config


import requests
import time
import threading
import websocket
import json


def request_by_requests(event, data: dict, headers: dict, full_address: str):
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
        print(f"[transmit] 未找到 self_id 为 {self_id} 的连接配置")
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
    if plugin_manager.before_request:
        for before_request_item in plugin_manager.before_request:
            event, method, data, platform, self_id = before_request_item(event, method, data, platform, self_id)
    # 发送POST请求

    event, data, headers, full_address, response_dict = request_by_requests(event, data, headers, full_address)

    # 调用after_request
    if plugin_manager.after_request:
        for after_request_item in plugin_manager.after_request:
            event, method, data, platform, self_id, response_dict = after_request_item(event, method, data, platform, self_id, response_dict)


def on_message(ws: websocket.WebSocketApp, message: str):
    from core import main
    data: dict = json.loads(message)
    # 展示登陆信息
    if data['op'] == 4:
        # print(data)
        print("[transmit] Satori driver connection successful.")
        for login_info in data['body']['logins']:
            name = login_info['user'].get('name', login_info['user']['id'])
            status = login_info['status']
            status_desc = "\033[32monline\033[0m" if status == 1 else "\033[31moffline\033[0m"
            print(f"[transmit] [{name}] login [{login_info['platform']}] status: {status_desc}")

    # event 事件
    if data['op'] == 0:
        thread = threading.Thread(target=main, args=(data["body"],))
        thread.start()


class WebsocketLink:
    def __init__(self, connection_config):
        self.websocket = None
        self.token: str = connection_config['token']
        self.full_address: str = f'ws://{connection_config["address"]}/events'
        # print(self.full_address)
        # 启动心跳包发送
        self.heartbeat_thread = threading.Thread(target=self.while_send_ping_packet)
        self.heartbeat_thread.start()

    # 心跳保活 自动重连
    def while_send_ping_packet(self):
        # 连接建立后，每隔 10s 向 SDK 发送一次 PING 信令
        while True:
            try:
                # 心跳间隔 < 10s
                time.sleep(5)
                if self.websocket and self.websocket.sock:
                    identify_packet = {
                        "op": 1,
                        "body": {
                            "美少女客服": "我是一只心跳猫猫"
                        }
                    }
                    self.websocket.send(json.dumps(identify_packet))
                else:
                    # 连接已关闭，执行重新连接逻辑
                    self.run()
            except Exception as e:
                print(f"发送心跳包时发生异常: {e}")

    # 认证 IDENTIFY 信令：连接建立后，在 10s 内发送一个 IDENTIFY 信令，用于鉴权和恢复会话
    def on_open(self, ws: websocket.WebSocketApp):
        identify_packet = {
            "op": 3,
            "body": {
                "token": self.token,
                "sequence": None
            }
        }
        ws.send(json.dumps(identify_packet))
        # print(f"[websocket] 尝试连接到 Satori 驱动器 ...")

    def run(self):
        try:
            # 连接 ws
            self.websocket = websocket.WebSocketApp(self.full_address, on_message=on_message)
            # 认证 IDENTIFY 信令
            self.websocket.on_open = self.on_open
            # 跑！
            self.websocket.run_forever()
        except Exception as e:
            print(f"An error occurred: {e}\nfunction' object has no attribute 'WebSocketApp 可能是账号配置错误")


def websocket_():
    connections = config["websocket_client"]["connections"]
    if not connections:
        print("\033[31m[transmit] websocket_client 未配置任何连接信息\033[0m")
        return
    for connection_config in connections:
        # 来自文件 websocket_link
        websocket_ink = WebsocketLink(connection_config)
        t = threading.Thread(target=websocket_ink.run)
        t.daemon = True
        t.start()


def start_ws():
    t = threading.Thread(target=websocket_)
    t.daemon = True
    t.start()


start_ws()







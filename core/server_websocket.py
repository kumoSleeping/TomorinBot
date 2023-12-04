import time
import threading
import websocket
import json

from session import main


def on_message(ws: websocket.WebSocketApp, message: str):
    data: dict = json.loads(message)
    # 展示登陆信息
    if data['op'] == 4:
        # print(data)
        print("Satori驱动器连接成功！")
        for login_info in data['body']['logins']:
            name = login_info['user'].get('name', login_info['user']['id'])
            status = login_info['status']
            status_desc = "运行中" if status == 1 else "waiting" if status == 2 else "未知状态"
            print(f"[logining_caller] [{name}] 上线 [{login_info['platform']}] 状态: {status_desc}")

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
        print(f"尝试连接到 Satori 驱动器 ...")

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


import json
import websocket
import threading
import os
import time

# 获取当前脚本的目录路径,将当前工作目录切换到脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from Tomorin import main
from Soyorin import TOKEN, IP, PORT, SATORI_PATH, Heartbeat_cd
from Soyorin import Utils


# 注册 on_message 事件
def on_message(ws, message):
    data = json.loads(Utils.unescape_special_characters(message))
    # 展示登陆信息
    if data['op'] == 4:
        print("Satori驱动器连接成功！")
        for login_info in data['body']['logins']:
            print(f"[{login_info['user']['name']}] 已上线平台 [{login_info['platform']}]!")
    # event 事件
    if data['op'] == 0:
        thread = threading.Thread(target=main, args=(data["body"],))
        thread.start()


class SatoriBot:
    def __init__(self):
        self.websocket = None
        self.token = TOKEN
        self.ws_url = f"ws://{IP}:{PORT}{SATORI_PATH}/v1/events"

        # 启动心跳包发送
        self.heartbeat_thread = threading.Thread(target=self.while_send_ping_packet)
        self.heartbeat_thread.start()

    # 心跳保活：连接建立后，每隔 10s 向 SDK 发送一次 PING 信令
    def while_send_ping_packet(self):
        while True:
            time.sleep(Heartbeat_cd)
            identify_packet = {
                "op": 1,
                "body": {
                    "美少女客服": "我是一只心跳猫猫"
                }
            }
            self.websocket.send(json.dumps(identify_packet))

    # 认证 IDENTIFY 信令：连接建立后，在 10s 内发送一个 IDENTIFY 信令，用于鉴权和恢复会话
    def on_open(self, ws):
        identify_packet = {
            "op": 3,
            "body": {
                "token": self.token,
                "sequence": None
            }
        }
        ws.send(json.dumps(identify_packet))
        print("尝试连接到 Satori 驱动器...")

    def run(self):
        try:
            # 连接 ws
            self.websocket = websocket.WebSocketApp(self.ws_url, on_message=on_message)
            # 认证 IDENTIFY 信令
            self.websocket.on_open = self.on_open
            # 跑！
            self.websocket.run_forever()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            exit()


if __name__ == "__main__":
    satori_bot = SatoriBot()
    satori_bot.run()

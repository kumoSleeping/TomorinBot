import json
import websocket
import threading
import os
import time
import yaml
import requests
import inspect
import sys


# 获取当前脚本的目录路径
# 获取当前代码所在文件的位置（包括文件名）
current_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
# 获取当前代码所在文件的目录
current_file_directory = os.path.dirname(current_file_path)
# 获取上一级目录 也就是主目录
parent_directory = os.path.dirname(current_file_directory)
# 将当前工作目录切换到 上一级目录 也就是主目录
os.chdir(parent_directory)
sys.path.append(parent_directory)

from tomorin import main

ascii_dev = '''
 ██████╗ ███████╗██╗   ██╗ 
 ██╔══██╗██╔════╝██║   ██║ 
 ██║  ██║█████╗  ██║   ██║ 
 ██║  ██║██╔══╝  ╚██╗ ██╔╝ 
 ██████╔╝███████╗ ╚████╔╝ 
 ╚═════╝ ╚══════╝  ╚═══╝  
DEV模式启动，将会转发消息给 dev.py。
所有组件日志将 dev.py 显示。
        '''
ascii_tmr = '''
     __________________________________
    |                                  |\ 
    |   ████████╗███╗   ███╗██████╗    | |
    |   ╚══██╔══╝████╗ ████║██╔══██╗   | |
    |      ██║   ██╔████╔██║██████╔╝   | |
    |      ██║   ██║╚██╔╝██║██╔══██╗   | |
    |      ██║   ██║ ╚═╝ ██║██║  ██║   | |
    |      ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝   | |
    |                                  | |
    |            运行常规模式
    |     欢迎使用 TomorinBOT 项目模版
    |                                  | |
    |                                  | |
    |                                  | |
    |              春日影                
    |                                  | |
    |                                  | |
    |                                  | |
    |__________________________________| |
     \__________________________________\|   

            '''

config: dict = yaml.safe_load(open(str(parent_directory) + '/config.yml', encoding='utf-8'))

DEV_URL = config["dev"]["endpoint"]
dev = False
try:
    response = requests.get(f'http://localhost:{config["dev"]["port"]}')
    print(ascii_dev)
    dev = True

except requests.exceptions.ConnectionError:
    print(ascii_tmr)
    dev = False


def send_2_dev_flask(data_body):
    endpoint = DEV_URL  # 替换为实际API endpoint
    headers = {
        'Content-Type': 'application/json',
    }
    requests.post(endpoint, json=json.dumps(data_body), headers=headers, verify=True)


def on_message(ws: websocket.WebSocketApp, message: str):
    # data = json.loads(Utils.unescape_special_characters(message))
    data: dict = json.loads(message)
    # 展示登陆信息
    if data['op'] == 4:
        print("Satori驱动器连接成功！")
        for login_info in data['body']['logins']:
            print(f"[{login_info['user']['name']}] 已上线平台 [{login_info['platform']}]!")
    # event 事件
    if data['op'] == 0:
        if dev:
            thread = threading.Thread(target=send_2_dev_flask, args=(data["body"],))
            thread.start()
        else:
            thread = threading.Thread(target=main, args=(data["body"],))
            thread.start()


class SatoriBot:
    def __init__(self, connection_config):
        self.websocket = None
        self.token: str = connection_config['token']
        self.url: str = connection_config['url']
        self.version: str = connection_config['version']
        self.heartbeat_cd: int = connection_config['HeartbeatInterval']

        self.ws_url = f"{self.url}/{self.version}/events"

        # 启动心跳包发送
        self.heartbeat_thread = threading.Thread(target=self.while_send_ping_packet)
        self.heartbeat_thread.start()

    # 心跳保活：连接建立后，每隔 10s 向 SDK 发送一次 PING 信令
    def while_send_ping_packet(self):
        while True:
            try:
                time.sleep(self.heartbeat_cd)
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
                # 发生异常时，也执行重新连接逻辑

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
            self.websocket = websocket.WebSocketApp(self.ws_url, on_message=on_message)
            # 认证 IDENTIFY 信令
            self.websocket.on_open = self.on_open
            # 跑！
            self.websocket.run_forever()
        except Exception as e:
            print(f"An error occurred: {e}")


if "connections" in config:
    connections = config["connections"]
    for connection_config in connections:
        satori_bot = SatoriBot(connection_config)
        t = threading.Thread(target=satori_bot.run)
        t.start()




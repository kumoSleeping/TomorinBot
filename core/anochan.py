import json
import websocket
import threading
import os
import time
import yaml
import requests

# 获取当前脚本的目录路径
script_directory = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录的绝对路径
# 将当前工作目录切换到脚本所在的目录
os.chdir(script_directory)


from tomorin import main


parent_directory = os.path.dirname(script_directory)  # 获取上一级目录的绝对路径

config = yaml.safe_load(open(str(parent_directory) + '/config.yml', encoding='utf-8'))

DEV_URL = config["dev"]["endpoint"]
dev = False
try:
    response = requests.get(f'http://localhost:{config["dev"]["port"]}')
    if response.status_code:
        ascii_ = '''
 ██████╗ ███████╗██╗   ██╗ 
 ██╔══██╗██╔════╝██║   ██║ 
 ██║  ██║█████╗  ██║   ██║ 
 ██║  ██║██╔══╝  ╚██╗ ██╔╝ 
 ██████╔╝███████╗ ╚████╔╝ 
 ╚═════╝ ╚══════╝  ╚═══╝  
DEV模式启动，将会转发消息给 dev.py。
所有组件日志将 dev.py 显示。
        '''
        print(ascii_)
        dev = True

except requests.exceptions.ConnectionError:
    ascii_ = '''
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
    print(ascii_)
    dev = False


def send_2_dev_flask(data_body):
    endpoint = DEV_URL  # 替换为实际API endpoint
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(endpoint, json=json.dumps(data_body), headers=headers, verify=True)


def on_message(ws, message):
    # data = json.loads(Utils.unescape_special_characters(message))
    data = json.loads(message)
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
        self.token = connection_config['token']
        self.url = connection_config['url']
        self.version = connection_config['version']
        self.Heartbeat_cd = connection_config['HeartbeatInterval']

        self.ws_url = f"{self.url}/{self.version}/events"

        # 启动心跳包发送
        self.heartbeat_thread = threading.Thread(target=self.while_send_ping_packet)
        self.heartbeat_thread.start()

    # 心跳保活：连接建立后，每隔 10s 向 SDK 发送一次 PING 信令
    def while_send_ping_packet(self):
        while True:
            try:
                time.sleep(self.Heartbeat_cd)
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
    def on_open(self, ws):
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




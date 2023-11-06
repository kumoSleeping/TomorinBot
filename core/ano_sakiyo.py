from flask import Flask, request, jsonify, make_response
import json
import websocket
import threading
import os
import time
import yaml
import requests
import inspect
import sys


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

config: dict = yaml.safe_load(open(str(parent_directory) + '/config.yml', encoding='utf-8'))


def on_message(ws: websocket.WebSocketApp, message: str):
    data: dict = json.loads(message)
    # 展示登陆信息
    if data['op'] == 4:
        print("Satori驱动器连接成功！")
        for login_info in data['body']['logins']:
            print(f"[{login_info['user']['name']}] 已上线平台 [{login_info['platform']}]!")
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
            self.websocket = websocket.WebSocketApp(self.full_address, on_message=on_message)
            # 认证 IDENTIFY 信令
            self.websocket.on_open = self.on_open
            # 跑！
            self.websocket.run_forever()
        except Exception as e:
            print(f"An error occurred: {e}\nfunction' object has no attribute 'WebSocketApp 可能是账号配置错误")


app = Flask(__name__)


@app.route('/start_websocket', methods=['GET'])
def websocket_():
    connections = config["connections"]
    for connection_config in connections:
        if connection_config["link_way"] == 'websocket':
            websocket_ink = WebsocketLink(connection_config)
            t = threading.Thread(target=websocket_ink.run)
            t.daemon = True
            t.start()
        else:
            continue
    return 'All websockets connected.'


@app.route('/', methods=['POST'])
def webhook_():
    try:
        data = request.json
        main(data)
    except:
        print('测试，来自js')
        data = json.loads((request.json))
        main(data)
    return 'ok'


if __name__ == '__main__':
    cd = 1
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not config["server"]["reload"]:
        print(f'将在{cd}s后唤醒ws连接')

        def start_ws():
            time.sleep(cd)
            requests.get(f'http://{config["server"]["host"]}:{config["server"]["local_port"]}/start_websocket')

        t = threading.Thread(target=start_ws)
        t.daemon = True
        t.start()
    app.run(host=config["server"]["host"], port=config["server"]["local_port"], debug=config["server"]["reload"])







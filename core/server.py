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


# # 获取当前代码所在文件的位置（包括文件名）
# current_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
# # 获取当前代码所在文件的目录
# current_file_directory = os.path.dirname(current_file_path)
# # 获取上一级目录 也就是主目录
# parent_directory = os.path.dirname(current_file_directory)
# # 将当前工作目录切换到 上一级目录 也就是主目录
# os.chdir(parent_directory)
# sys.path.append(parent_directory)


# 获取当前文件的父目录并切换工作目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
os.chdir(parent_directory)
sys.path.append(parent_directory)


from session import main
from server_websocket import WebsocketLink
from config import config

app = Flask(__name__)


@app.route('/start_websocket', methods=['GET'])
def websocket_():
    connections = config["connections"]
    for connection_config in connections:
        if connection_config["link_way"] == 'websocket':
            # 来自文件 websocket_link
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







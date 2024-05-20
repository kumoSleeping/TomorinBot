from core.__main__ import config
from core.classes.event import Event
from core.classes.utils import log
from core.classes.utils import c

import websocket
import json
import threading
import gc
import time


from __main__ import initialize_manager


def build_session(data: dict):
    """
    构建会话的流程，会在 ws 接收到消息时调用。

    :param data: satori 标准事件数据
    :return: None
    """
    try:
        event: Event = Event(data)

        if initialize_manager._event_built:
            for after_event_item in initialize_manager._event_built:
                if event:
                    event = after_event_item(event)
        for loaded_func_item in initialize_manager._satori_event:
            if initialize_manager._satori_event:
                plugin_thread = threading.Thread(target=loaded_func_item, args=(event,))
                plugin_thread.start()

    except Exception as e:
        log.error('Error occurred.')
        raise e

    finally:
        # 无论如何都会执行的清理代码
        gc.collect()


def on_message(ws, message):
    # 按照要求，这里 ws 和 message 都是必须的参数，而且类型为 any （为什么啊！）
    data: dict = json.loads(message)
    # 展示登陆信息
    if data["op"] == 4:
        log.success("satori driver connected")
        for login_info in data["body"]["logins"]:
            name = login_info["user"].get("name", login_info["user"]["id"])
            if name == '':
                name = 'SOMEBOT'
            status = login_info["status"]
            (
                log.success(f"bot {c.bright_yellow}{c.style.bold}{c.style.underline}{name}{c.reset} login {c.bright_green}{login_info['platform']}{c.reset}")
                if status == 1
                else log.red(f"{name} login {login_info['platform']}")
            )

    # event 事件
    if data["op"] == 0:
        thread = threading.Thread(target=build_session, args=(data["body"],))
        thread.start()


class WebsocketLink:
    def __init__(self, connection_config):
        self.websocket = None
        self.token: str = connection_config["token"]
        self.full_address: str = f'ws://{connection_config["address"]}/v1/events'  # 目前只支持 v1
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
                        "body": {"美少女客服": "我是一只心跳猫猫"},
                    }
                    self.websocket.send(json.dumps(identify_packet))
                else:
                    # 连接已关闭，执行重新连接逻辑
                    self.run()
            except Exception as e:
                log.error(f"发送心跳包时发生异常: {e}")

    # 认证 IDENTIFY 信令：连接建立后，在 10s 内发送一个 IDENTIFY 信令，用于鉴权和恢复会话
    def on_open(self, ws: websocket.WebSocketApp):
        identify_packet = {"op": 3, "body": {"token": self.token, "sequence": None}}
        ws.send(json.dumps(identify_packet))
        # log.debug(f"尝试连接到 Satori 驱动器 ...")

    def run(self):
        try:
            log.info(f'link start...')
            # 连接 ws
            self.websocket = websocket.WebSocketApp(
                url=self.full_address, on_message=on_message
            )
            # 认证 IDENTIFY 信令
            self.websocket.on_open = self.on_open
            # 跑！
            self.websocket.run_forever()
        except Exception as e:
            log.error(
                f"{e}\nfunction' object has no attribute 'WebSocketApp 可能是账号配置错误"
            )


def websocket_():
    try:
        config.need(
            "websocket_connections",
            [
                {
                    "self_ids": ["11111", "22222"],
                    "address": "127.0.0.1:5140/satori",
                    "http_protocol": "http",
                    "token": "Your_token",
                }
            ],
        )

        connections = config.get_key("websocket_connections")
        if not connections:
            log.warning("\033[31m websocket_client 未配置任何连接信息\033[0m")
            return
        for connection_config in connections:
            # 来自文件 websocket_link
            websocket_ink = WebsocketLink(connection_config)
            t = threading.Thread(target=websocket_ink.run)
            t.daemon = True
            t.start()
    except Exception as e:
        log.error(f"{e}\nWebsocket-client： Please check your configuration file.")
        return


def start_ws():
    t = threading.Thread(target=websocket_)
    t.daemon = True
    t.start()

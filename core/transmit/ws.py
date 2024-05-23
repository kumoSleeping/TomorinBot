import asyncio
import websockets
import json
import threading

from core.__main__ import config
from core.classes.log import log, c
from core.invoker.dispatcher import build_session_async, build_session_sync


async def on_message(websocket, path, message):
    data = json.loads(message)
    if data["op"] == 4:
        log.success(f"connected {c.bright_red}Satori Driver{c.reset}")
        for login_info in data["body"]["logins"]:
            name = login_info["user"].get("name", login_info["user"]["id"])
            if name == '':
                name = 'NO-NAME-BOT'
            status = login_info["status"]
            if status == 1:
                log.success(f"apply {c.bright_red}Satori Driver{c.reset} {c.bright_yellow}{c.style.bold}{c.style.underline}{name}{c.reset} login {c.bright_green}{login_info['platform']}{c.reset}.")
            else:
                log.warning(f"apply {c.bright_red}Satori Driver{c.reset} {c.bright_yellow}{c.style.bold}{c.style.underline}{name}{c.reset} sleep in {c.bright_green}{login_info['platform']}{c.reset}.")
    if data["op"] == 0:
        # sync with threading
        threading.Thread(target=build_session_sync, args=(data["body"],)).start()
        # async
        task = asyncio.create_task(build_session_async(data["body"]))


class WebsocketLink:
    def __init__(self, connection_config):
        self.token = connection_config["token"]
        self.full_address = f'ws://{connection_config["address"]}/v1/events'
        self.websocket = None

    async def send_ping(self):
        while True:
            try:
                await asyncio.sleep(5)
                if self.websocket:
                    identify_packet = {
                        "op": 1,
                        "body": {"美少女客服": "我是一只心跳猫猫"},
                    }
                    await self.websocket.send(json.dumps(identify_packet))
            except Exception as e:
                log.error(f"发送心跳包时发生异常: {e}")
                break

    async def on_open(self, websocket):
        identify_packet = {"op": 3, "body": {"token": self.token, "sequence": None}}
        await websocket.send(json.dumps(identify_packet))

    async def run(self):
        async with websockets.connect(self.full_address) as websocket:
            self.websocket = websocket
            await self.on_open(websocket)
            await asyncio.gather(
                self.send_ping(),
                self.receive_messages(websocket)
            )

    async def receive_messages(self, websocket):
        async for message in websocket:
            await on_message(websocket, self.full_address, message)


async def websocket_():
    try:
        config.need(
            "websocket_connections",
            [
                {
                    "self_ids": ["11111", "22222"],
                    "address": "127.0.0.1:5140/satori/v1",
                    "http_protocol": "http",
                    "token": "Your_token",
                }
            ],
        )
        connections = config.get_key("websocket_connections")
        if not connections:
            log.warning("websocket_client 未配置任何连接信息")
            return
        log.info(f'linking {c.bright_red}Satori Driver{c.reset} ...')
        # 启动所有WebSocket连接
        await asyncio.gather(
            *(WebsocketLink(config_ws).run() for config_ws in connections)
        )
    except Exception as e:
        log.error(f"{e}\nWebsocket-client: Please check your configuration file.")


async def start_ws():
    await websocket_()
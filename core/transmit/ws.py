import asyncio
import aiohttp
import json
import threading

from core.__main__ import config
from core.classes.log import log, c
from core.invoker.dispatcher import parse_event


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
                log.success(f"linked {c.bright_red}Satori Driver{c.reset} {c.bright_yellow}{c.style.bold}{c.style.underline}{name}{c.reset} login {c.bright_green}{login_info['platform']}{c.reset}.")
            else:
                log.warning(f"linked {c.bright_red}Satori Driver{c.reset} {c.bright_yellow}{c.style.bold}{c.style.underline}{name}{c.reset} sleep in {c.bright_green}{login_info['platform']}{c.reset}.")
    if data["op"] == 0:
        task = asyncio.create_task(parse_event(data["body"]))


class WebsocketLink:
    def __init__(self, connection_config):
        self.token = connection_config["token"]
        self.full_address = f'ws://{connection_config["address"]}/v1/events'
        self.session = aiohttp.ClientSession()
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
                    await self.websocket.send_json(identify_packet)
            except Exception as e:
                log.error(f"发送心跳包时发生异常: {e}")
                break

    async def on_open(self):
        identify_packet = {"op": 3, "body": {"token": self.token, "sequence": None}}
        await self.websocket.send_json(identify_packet)

    async def run(self):
        while True:
            try:
                async with self.session.ws_connect(self.full_address) as self.websocket:
                    log.info(f'linking {c.bright_red}Satori Driver{c.reset} ...')
                    await self.on_open()
                    await asyncio.gather(
                        self.send_ping(),
                        self.receive_messages()
                    )
            except aiohttp.WSServerHandshakeError as e:
                log.error(f"WebSocket handshake error: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)
            except OSError as e:
                log.error(f"Network error: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                log.error(f"An unexpected error occurred: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)

    async def receive_messages(self):
        async for msg in self.websocket:
            if msg.type == aiohttp.WSMsgType.TEXT:
                await on_message(self.websocket, self.full_address, msg.data)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

    async def close(self):
        await self.session.close()


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
        links = [WebsocketLink(config_ws) for config_ws in connections]
        # 启动所有连接
        await asyncio.gather(*(link.run() for link in links))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # 确保所有 session 被关闭
        await asyncio.gather(*(link.close() for link in links if link.session))


async def start_ws():
    await websocket_()


import asyncio
import json
import websockets
import threading
import os

# 获取当前脚本的目录路径,将当前工作目录切换到脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from Tomorin import main
from Soyorin import TOKEN, IP, PORT, SATORI_PATH, Heartbeat_cd
from Soyorin import Utils

'''
Ano.py · receive
程序启动入口
对「satori」协议进行连接 / session获取 / 心跳保活
为每个 session 启动 Main(data)
'''


async def handle_data(data):
    # print("Dev中信息：", data)
    if data['op'] == 4:
        print("Satori驱动器连接成功！")
        for login_info in data['body']['logins']:
            print(f"[{login_info['user']['name']}] 已上线平台 [{login_info['platform']}]!")

    if data['op'] == 0:
        # 当收到 消息类event，调用 ./Tmorin.py 的 Main() 并传入 data
        thread = threading.Thread(target=main, args=(data["body"],))
        thread.start()
    if data['op'] == 2:
        # print('[心跳状态：存活]')
        pass


class SatoriBot:
    def __init__(self):
        self.websocket = None
        self.token = TOKEN
        self.ws_url = f"ws://{IP}:{PORT}{SATORI_PATH}/v1/events"

    async def while_send_ping_packet(self):
        while True:
            await self.send_ping_packet()
            await asyncio.sleep(Heartbeat_cd)  # 使用 asyncio.sleep 代替 time.sleep

    async def send_ping_packet(self):
        identify_packet = {
            "op": 1,
            "body": {
                "美少女客服": "我是一只心跳猫猫"
            }
        }
        await self.websocket.send(json.dumps(identify_packet))

    async def connect(self):
        self.websocket = await websockets.connect(self.ws_url)
        await self.send_identify_packet()
        asyncio.create_task(self.while_send_ping_packet())  # 使用 asyncio.create_task 启动异步函数

    async def send_identify_packet(self):
        identify_packet = {
            "op": 3,
            "body": {
                "token": self.token,
                "sequence": None
            }
        }
        await self.websocket.send(json.dumps(identify_packet))
        print("尝试连接到 Satori 驱动器...")

    async def receive_message(self):
        while True:
            try:
                message = await self.websocket.recv()
                data = json.loads(Utils.unescape_special_characters(message))
                await handle_data(data)
            except websockets.ConnectionClosed as e:
                print(f"WebSocket connection closed. ")
                break

    async def run(self):
        try:
            await self.connect()
            await self.receive_message()
        finally:
            exit()


satori_bot = SatoriBot()
asyncio.get_event_loop().run_until_complete(satori_bot.run())






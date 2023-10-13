import asyncio
import json
import websockets
import threading

from .Tomorin import main
from server import TOKEN, IP, PORT, Heartbeat_cd
from .utils.utils import Utils

'''
Ano.py · receive
程序启动入口
对「satori」协议进行连接 / session获取 / 心跳保活
为每个 session 启动 Main(data)
'''


async def handle_data(data):
    # print("Dev中信息：", data)
    if data['op'] == 4:
        platform = data['body']['logins'][0]['platform']
        bot_name = data['body']['logins'][0]['user']['name']
        print(f"Satori驱动器连接成功，{bot_name} 已上线 [{platform}] ！")
    if data['op'] == 0:
        # 这里开了一个线程，用于处理消息，process_message在隔壁c_p.py里面，相当于利用外部文件劫持了本线程的函数，本身不影响ws线程整体运行
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
        self.ws_url = f"ws://{IP}:{PORT}/v1/events"
        # self.session = aiohttp.ClientSession()

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
                "sequence": None  # You may set a sequence if needed for session recovery
            }
        }
        await self.websocket.send(json.dumps(identify_packet))
        print("尝试连接到Satori驱动器...")

    async def receive_message(self):
        while True:
            try:
                message = await self.websocket.recv()
                # data = json.loads(message)
                # 这里直接unescape_special_characters可能会导致混淆
                data = json.loads(Utils.unescape_special_characters(message))
                # handle_data在上面
                await handle_data(data)
            except websockets.ConnectionClosed:
                print("WebSocket connection closed.")
                break

    async def run(self):
        try:
            await self.connect()
            await self.receive_message()
        finally:
            exit()
        #     await self.session.close()


satori_bot = SatoriBot()
asyncio.get_event_loop().run_until_complete(satori_bot.run())






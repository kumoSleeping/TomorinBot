import asyncio
from random import randint

from tmrn import app
from tmrn import cmd_select
from tmrn import sub_input, sub_channel_input
from satori import Event, EventType, E
from satori.client import Account
from arclet.alconna import Alconna, Args, output_manager, CommandMeta


@app.register_on(EventType.MESSAGE_CREATED)
async def on_message_(account: Account, event: Event):
    if cmd_select(event, prefix=['/', '']) == 'ping':
        send_msg = E.text('pong').dumps()

        # from PIL import Image
        # import io
        # img = Image.new('RGB', (100, 100), color='red')
        # img_bytes = io.BytesIO()
        # img.save(img_bytes, format='PNG')
        # send_msg += E.image(raw=img_bytes, mime='image/png').dumps()

        # 发送消息
        await account.send(event, send_msg)


@app.register_on(EventType.MESSAGE_CREATED)
async def on_message_miao(account: Account, event: Event):
    if 't' == cmd_select(event, prefix=['.'], white_user='1528593481'):
        await account.send(event, 'y/n?')
        while True:
            event_ = await sub_input(event, timeout=60)

            if not event_:  # 如果超时或没有输入
                await account.send(event, '没有收到输入，会话结束。')
                break  # 退出循环

            match cmd_select(event_):
                case 'y':
                    await account.send(event_, '🐱！')
                    break
                case 'n':
                    await account.send(event_, '退出会话。')
                    break
                case _:
                    await account.send(event_, '请输入 y 或 n。')


@app.register_on(EventType.MESSAGE_CREATED)
async def on_message_miao_1(account: Account, event: Event):
    output_manager.set_action(lambda msg: asyncio.create_task(account.send(event, msg)))
    if msg := cmd_select(event):
        if (res := Alconna(['猜数字', 'csz'],Args['max_int;?', int, 100],meta=CommandMeta(compact=True,description="猜猜数字",)).parse(msg)).matched:
            await account.send(event, f'请输入一个 1-{res.max_int} 之间的整数。')
            number = randint(1, res.max_int)

            async def game_logic():
                while True:
                    event_ = await sub_channel_input(event)
                    if not event_:
                        continue

                    if rpl := cmd_select(event_):
                        if rpl == '不猜了':
                            await account.send(event_, '不猜就不猜😭')
                            return
                        if not rpl.isdigit():
                            continue

                        if (guess := int(rpl)) == number:
                            await account.send(event_, '🎉 正确！')
                            return
                        elif number < guess:
                            await account.send(event_, '大了，请再猜一次。')
                        else:
                            await account.send(event_, '小了，请再猜一次。')

            try:
                await asyncio.wait_for(game_logic(), timeout=60)
            except asyncio.TimeoutError:
                await account.send(event, '时间到！游戏结束。正确答案是：' + str(number))
        else:
            if res.head_matched and str(res.error_info) != 'help':
                await account.send(event, '参数错误：' + str(res.error_info))




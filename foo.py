import asyncio
from random import randint

from tmrn import cmd_select, app, sub_input, sub_channel_input
from satori import Event, EventType
from satori.client import Account
from arclet.alconna import Alconna, Args, output_manager, CommandMeta


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

    def send_msg(msg):
        asyncio.create_task(account.send(event, msg))

    output_manager.set_action(send_msg)

    if msg := cmd_select(event, white_user='1528593481'):
        if (res := Alconna(['猜数字'],Args['max_int;?', int, 100],meta=CommandMeta(compact=True,description="猜猜数字",)).parse(msg)).matched:
            await account.send(event, f'请输入一个 1-{res.max_int} 之间的整数。')
            number = randint(1, res.max_int)

            async def game_logic():
                while True:
                    event_ = await sub_channel_input(event)
                    if not event_:
                        continue

                    if rpl := cmd_select(event_):
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
            if res.head_matched:
                if str(res.error_info) != 'help':
                    await account.send(event, '参数错误：' + str(res.error_info))




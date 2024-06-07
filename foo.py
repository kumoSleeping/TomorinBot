from tmrn import cmd_select, app, sub_input
from satori import Event, EventType
from satori.client import Account


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


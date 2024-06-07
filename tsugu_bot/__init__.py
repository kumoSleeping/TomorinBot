from satori import Event, WebsocketsInfo, EventType
from satori.element import E
from satori.client import Account, App
from tmrn import app, cmd_select
from tsugu import handler_raw_async


@app.register_on(EventType.MESSAGE_CREATED)
async def on_message_(account: Account, event: Event):
    if msg := cmd_select(event, prefix=['/', ''], white_user='1528593481'):
        res = await handler_raw_async(msg, event.user.id, 'red',event.channel.id)
        if not res:
            return
        modified_results = []
        for item in res:
            if item.get('type') == 'string':
                modified_results.append(item['string'])
            elif item.get('type') == 'base64':
                base_64_str = item['string']
                modified_results.append(E.image(url=f'data:image/jpg;base64,{base_64_str}').dumps())
        await account.send(event, modified_results)
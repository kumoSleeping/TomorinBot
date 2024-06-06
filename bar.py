from satori import Event, WebsocketsInfo, EventType
from satori.element import E
from satori.client import Account, App
from tmrn import app, cmd_select


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




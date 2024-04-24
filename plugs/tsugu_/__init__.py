import mods
import tsugu
import base64
from datetime import datetime


tsugu.config.backend = 'http://127.0.0.1:3000'


@mods.on.message_created
def tsugu_plug(event: mods.Event):
    if res := mods.match_command(event, '', limit_admin=True, limit_at=True):
        time_node_1 = datetime.now()
        rpl = tsugu.handler(res.text, event.user.id, 'red', event.channel.id)
        if not rpl:
            return
        modified_results = []
        for item in rpl:
            if isinstance(item, str):
                modified_results.append(item)
            elif isinstance(item, bytes):
                modified_results.append(f'<img src="data:image/png;base64,{base64.b64encode(item).decode()}"/>')

        time_node_2 = datetime.now()
        # 只保留到几.xx秒
        seconds = (time_node_2 - time_node_1).total_seconds()
        # 保留2位小数
        seconds = round(seconds, 2)
        event.message_create(mods.h.quote(event.message.id) + ''.join(modified_results) + f'\n[耗时: {seconds}s]')


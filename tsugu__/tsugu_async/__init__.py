from core.interfaces import on, Event
import tsugu
from datetime import datetime

from tsugu_api import settings
from pil_utils import Text2Image
from command_matcher import match_command
from satori import E


def escape_html(text, direction='f'):
    escape_characters = {
        '"': '&quot;',
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;'
    }

    if direction == 'f':
        for char, escape in escape_characters.items():
            text = text.replace(char, escape)
    elif direction == 'b':
        for char, escape in escape_characters.items():
            text = text.replace(escape, char)
    else:
        raise ValueError("Direction must be 'forward' or 'backward'")

    return text


@on.message_created
async def tsugu_plug(event: Event):
    if res := match_command(event, '', limit_admin=True):
        time_node_1 = datetime.now()
        rpl = await tsugu.handler_raw_async(res.text, event.user.id, 'red', event.channel.id)
        if not rpl:
            return
        modified_results = []
        for item in rpl:
            if item.get('type') == 'string':
                modified_results.append(item['string'])
            elif item.get('type') == 'base64':
                base_64_str = item['string']
                # modified_results.append(f'<img src="data:image/png;base64,{base_64_str}"/>')
                modified_results.append(E.image(url=f'data:image/png;base64,{base_64_str}'))
        if len(modified_results) == 1 and '<img src=' not in modified_results[0]:
            if len(modified_results[0]) > 40:
                img = Text2Image.from_text(modified_results[0], 30, spacing=10).to_image(bg_color="white")
                modified_results[0] = E.image(img.tobytes())

        time_node_2 = datetime.now()
        seconds = (time_node_2 - time_node_1).total_seconds()
        seconds = round(seconds, 2)
        await event.message_create(E.quote(event.message.id) + ''.join(modified_results) + f'\n[耗时: {seconds}s]')






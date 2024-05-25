import mods
from mods import h, on, Event
import tsugu
import base64
import time
from datetime import datetime

from tsugu_api import settings
from pil_utils import Text2Image

settings.use_easy_bg = False


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


@mods.on.message_created
def tsugu_plug(event: mods.Event):
    if res := mods.match_command(event, '', limit_admin=True):
        time_node_1 = datetime.now()
        rpl = tsugu.handler_raw(res.text, event.user.id, 'red', event.channel.id)
        if not rpl:
            return
        modified_results = []
        for item in rpl:
            if item.get('type') == 'string':
                modified_results.append(item['string'], 'f')
            elif item.get('type') == 'base64':
                base_64_str = item['string']
                modified_results.append(f'<img src="data:image/png;base64,{base_64_str}"/>')
        if len(modified_results) == 1 and '<img src=' not in modified_results[0]:
            if len(modified_results[0]) > 20:
                img = Text2Image.from_text(modified_results[0], 30, spacing=10).to_image(bg_color="white")
                modified_results[0] = mods.h.image(img)

        time_node_2 = datetime.now()
        seconds = (time_node_2 - time_node_1).total_seconds()
        seconds = round(seconds, 2)
        event.message_create(mods.h.quote(event.message.id) + ''.join(modified_results) + f'\n[耗时: {seconds}s]')


@on.message_created
def zengsu(event: Event):
    if res := mods.match_command(event, '增速'):
        try:
            import requests
            import json
            import datetime
            import pytz

            def timestamp_to_beijing(timestamp):
                # 将毫秒级时间戳转换为秒级时间戳
                timestamp /= 1000
                utc_time = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
                beijing_tz = pytz.timezone('Asia/Shanghai')
                beijing_time = utc_time.astimezone(beijing_tz)
                return beijing_time.replace(tzinfo=None)  # 去除时区信息

            # 代理服务器的地址和端口
            proxy_host = '127.0.0.1'
            proxy_port = '7890'

            # 设置代理服务器
            proxies = {
                'http': f'http://{proxy_host}:{proxy_port}',
                'https': f'http://{proxy_host}:{proxy_port}'
            }

            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'if-none-match': 'W/"237b-sncLFgy8uCC9epTBS38Nb8Crw6c"',
                'referer': 'https://bestdori.com/tool/eventtracker/cn/t200 ',
                'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            }

            # params = {
            #     'server': '3',
            #     'event': '240',
            #     'tier': "100",
            # }
            #
            # response = requests.get('https://bestdori.com/api/tracker/data', params=params, headers=headers,
            #                         proxies=proxies)
            # current_time = json.loads(response.text)["cutoffs"][-1]["time"]
            # print("北京时间:", timestamp_to_beijing(current_time), "更新")
            xian = int(res.text)
            # if xian not in [20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 5000]:
            #     return

            params = {
                'server': '3',
                'event': '240',
                'tier': f'{xian}',
            }

            response = requests.get('https://bestdori.com/api/tracker/data', params=params, headers=headers,
                                    proxies=proxies)
            result = json.loads(response.text)
            last_latest = result["cutoffs"][-2]["ep"]
            # 万为单位
            last_latest_ = int(last_latest / 10000)
            latest = result["cutoffs"][-1]["ep"]
            latest_ = int(latest / 10000)
            # print(f"t{xian}")
            # print("当前分数线:", latest, end=", ")
            # print(f"实时增速:{(latest - last_latest) * 2}/小时")
            res.send(f"当前 {res.text} 分数线: {last_latest} ({last_latest_}万), 实时增速: {(latest - last_latest) * 2}/小时({(latest_ - last_latest_) * 2}万/小时)")

        except Exception as e:
            print(e)




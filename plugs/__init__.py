import mods


@mods.on.guild_member_added
def _welcome_new_GOp(event):
    if event.channel.id == '928460620':
        event.message_create(f'点击欢迎')


import time


@mods.on.message_created
def echo(event):
    if not mods.is_admin(event.platform, event.user.id):
        return

    messages = event.message.content.split('/e ')[1:]
    for message in messages:
        event.message_create(message.strip())
        time.sleep(0.5)


@mods.on.message_created
def echo_bdb(event):
    if not mods.is_admin(event.platform, event.user.id):
        return
    if event.message.content == ' bdzt':
        event.message_create('笨蛋状态')
    if event.message.content == ' hbgl':
        event.message_create('伙伴管理')
    if res := mods.match_command(event, ' schb'):
        res.args = res.text.split()
        #         只保留数字
        res.args = [x for x in res.args if x.isdigit()]
        for i in list(set(res.args)):
            event.message_create(f'删除伙伴 {i}')
    if event.message.content.startswith(' hbth'):
        event.message_create('伙伴替换' + event.message.content[5:])
    if event.message.content == ' zsjd':
        event.message_create('转生进度')
    if event.message.content.startswith(' tb'):
        event.message_create('投币' + event.message.content[3:])


from PIL import Image, ImageDraw, ImageFont


@mods.on.message_created
def bzl_pic(event: mods.Event):
    # print(0)
    if res := mods.match_command(event, ['bzl'], allow_gap_less=True):
        # print(res)
        # print(1)
        if res.text.isdigit():
            # print(2)
            num = int(res.text)
            img = Image.open(mods.assets('bzl.png'))
            # 设置字体
            # print(mods.assets('font.ttf'))
            font = ImageFont.truetype(mods.assets('font.ttf'), 50)
            # 左上角写字，白色
            draw = ImageDraw.Draw(img)
            # 测量文字宽度
            width = draw.textlength(f'{num}名', font)
            draw.text((240 - width / 2, 275), f'{num}名', fill=(255, 255, 255), font=font)
            draw.text((1387 - width / 2, 448), f'{num + 1}名', fill=(255, 255, 255), font=font)
            # 保存
            res.send(mods.h.image(img))
            img.close()


import re
from bs4 import BeautifulSoup

bot_self_id = '211134009'
bdb_channel_id = '666808414'
bdb_platform = 'chronocat'
bd_id = '3260850774'


@mods.on.message_created
def auto_bdb(event):
    """
    全自动笨蛋读博机
    """
    # 保证发消息者是笨蛋，被quote者是bot
    #    print(event.message.content)
    # print(bd_id)
    if event.user.id != bd_id:
        # print('发消息者不是笨蛋')
        return
    try:
        soup = BeautifulSoup(event.message.content, 'xml')
        author_id = soup.find('quote').find('author')['id']
        if author_id != bot_self_id:
            # print('操作者不是bot')
            return
        msg: str = event.message.content
        # 你现在不许玩了！还要 4分8秒 之后才能玩笨蛋机哦 ！
        if msg.startswith('你现在不许玩了！') and msg.endswith('之后才能玩笨蛋机哦 ！'):
            return  # 不处理
        # 您当前拥有 263921 个笨蛋(>= 15 )， 不符合领取条件。 / 12 个笨蛋已经加入您的账户(冷却 4 小时)
        if (msg.endswith('不符合领取条件。') or msg.endswith('个笨蛋已经加入您的账户(冷却 4 小时)')):
            num = re.findall(r"\d+\.?\d*", mods.remove_all_xml(msg))
            num = int(num[0]) // 2
            event.message_create(f'投币{num}')
            return
        if msg.endswith('后才能领取笨蛋补助!') or msg.startswith('出错了！'):
            event.message_create(f'投币1000000000000000000000000000')
    except:
        pass


# 每天定时n次发消息
@mods.timer_do(
    ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
     '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'])
def clock1():
    event = Event()
    event.platform = bdb_platform
    event.self_id = bot_self_id
    event.message_create(channel_id=bdb_channel_id, content='笨蛋补助')


@mods.timer_do(['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'])
def chb():
    event = Event()
    event.platform = bdb_platform
    event.self_id = bot_self_id
    event.message_create(channel_id=bdb_channel_id, content='抽伙伴')
    event.message_create(channel_id=bdb_channel_id, content='删除伙伴 4')


chb()
clock1()

import json
import os

# print(mods.assets('gm.json'))
if os.path.exists(mods.assets('mcp.json')):
    with open(mods.assets('mcp.json'), 'r', encoding='utf-8') as f:
        data_gm = json.load(f)
else:
    data_gm: list = []
    with open(mods.assets('mcp.json'), 'w', encoding='utf-8') as f:
        json.dump(data_gm, f, ensure_ascii=False, indent=4)


def save_gm():
    with open(mods.assets('mcp.json'), 'w', encoding='utf-8') as f:
        json.dump(data_gm, f, ensure_ascii=False, indent=4)


@mods.on.message_created
def grp_mem(event: mods.Event):
    if res := mods.match_command(event, ['mcp add', 'mcpadd', '+mcp']):
        data_gm.append(res.text)
        save_gm()
        all_gm = '\n'.join([f'{i + 1}. {v}' for i, v in enumerate(data_gm)])
        res.send(all_gm)
    elif res := mods.match_command(event, ['mcp del', 'mcpdel', '-mcp']):
        try:
            del data_gm[int(res.text) - 1]
            save_gm()
            # res.send('删除成功')
            all_gm = '\n'.join([f'{i + 1}. {v}' for i, v in enumerate(data_gm)])
            res.send(all_gm)
        except:
            res.send('删除失败')
    elif res := mods.match_command(event, ['mcp']):
        all_gm = '\n'.join([f'{i + 1}. {v}' for i, v in enumerate(data_gm)])
        res.send(all_gm)


import pil_utils
import mods
import io


@mods.on.message_created
def test2(event: mods.Event):
    if res := mods.match_command(event, ['test2']):
        img = pil_utils.Text2Image.from_text(
            text="宝宝你是一个宝宝😊",
            fontsize=50,

        ).to_image(bg_color="white")
        # img_bytes_io = img.save_jpg()
        res.send(mods.h.image(img))


from plugs.tsugu_ import *
from plugs.rec import *

# @mods.on.before_event
# def deas(e):
#     print(e)
#     return e

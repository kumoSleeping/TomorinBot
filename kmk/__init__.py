import os

from kmk.gemini import initialize_chat_session, choice_list, send_request, process_response
from tmrn import app
from tmrn import cmd_select
from tmrn import sub_input, sub_channel_input
from satori import Event, EventType
from satori.client import Account
import contextvars
import random
import re

# 创建一个ContextVar来保存会话信息
channel_context = contextvars.ContextVar('channel_msg', default={})
channel_status_context = contextvars.ContextVar('channel_status_msg', default={})
session_id = initialize_chat_session()
active_int = 0


def delete_all_xml_in_str(str_):
    return re.sub(r'<[^>]+>', '', str_)


@app.register_on(EventType.MESSAGE_CREATED)
async def ctx_4_kmk(account: Account, event: Event):
    global active_int

    if event.channel.id not in ['666808414', '229588142', '499597152']:
        return

    if event.user.id == event.self_id:
        return

    if msg := delete_all_xml_in_str(event.message.content):
        print(msg)
        if 'kmk' == msg:
            active_int += 8
            await account.send(event, '我在')
            return

        elif 'kumoka' == msg:
            active_int += 10
            await account.send(event, '我在')
            return

        elif 'kumoka' in msg:
            active_int += 10

        elif 'kmk' in msg:
            active_int += 8

        add_active_int = [0, 0, 0, 0, 0.1, 0.1, 0]
        active_int += add_active_int[random.randint(0, 6)]
        print(active_int)
        # 获取当前上下文中的消息
        session_data = channel_context.get()

        # 获取当前频道的消息记录
        channel_messages = session_data.get(event.channel.id, {})

        # 更新消息内容，加入 event.id 和 event.user.id
        channel_messages[event.id] = {
            'user_id': event.user.id,
            'msg': msg
        }

        # 更新当前频道的消息记录
        session_data[event.channel.id] = channel_messages

        # 设置更新后的上下文
        channel_context.set(session_data)

        # 检查数量
        if len(channel_messages) > 15:
            # 删除最早的消息
            channel_messages.pop(next(iter(channel_messages)))

        if active_int > 1:
            quote_random_int = random.randint(0, 100)
            var_ = quote_random_int + active_int*3
            if var_ > 40:
                ctx = str(channel_context.get()[event.channel.id])
                print('start')
                active_int = 0
                resp = await send_request(session_id, '你要回答的消息:' + msg + '这里是上下文:' + ctx + '请直接说出你的回复，系统会直接发出去')
                if resp:
                    res_text = process_response(resp[0])
                    # 从res_text提取所有[img:xx]，提取出来的内容是xx，删掉[img:xx]，添加xx
                    img_list = re.findall(r'\[img:(.*?)]', res_text)
                    if len(img_list) > 0:
                        for img_text in img_list:
                            f_path = './kmk/img/' + img_text
                            # 读取 f_path 文件夹所有图片随机选择一个
                            img_text_ = f_path + '/' + random.choice(os.listdir(f_path))
                            # 读取图片
                            import base64
                            with open(img_text_, 'rb') as f:
                                base64_data = base64.b64encode(f.read()).decode()

                            # <img src="data:image/png;base64,{base64_data}"/>
                            print(img_text_)
                            img = f'<img src="data:image/png;base64,{base64_data}"/>'
                            res_text = res_text.replace(f'[img:{img_text}]', img)
                            await account.send(event, res_text)


        # async def check_msg(choice):
        #     session_id = initialize_chat_session()
        #     res = await choice_list(choice)
        #     if res and len(res) > 0:
        #         for i in res:
        #             ctx = str(channel_context.get()[event.channel.id])
        #             resp = await send_request(session_id, '你要回答的消息:'+choice[i]['msg']+'这里是上下文:'+ctx)
        #             print(process_response(resp[0]))

        # 检查数量，只保留最新的5条消息
        # if len(channel_status_messages) > 3:
            # 调用 check_msg 函数
            # print('start...')
            # start_ctx = session_data.get(event.channel.id)
            # channel_status_messages.clear()
            # await check_msg(start_ctx)
            # 删除所有消息

        # print(f"Current Context: {session_data.get(event.channel.id)}")
#         Current Context: {214098: {'user_id': '754746431', 'msg': '这雨是定了闹钟？'}, 214102: {'user_id': '1041219717', 'msg': '多冲几次榜就行（）'}, 214106: {'user_id': '1749596159', 'msg': '天天高温天天37℃'}, 214108: {'user_id': '804912964', 'msg': '查活动243'}, 214114: {'user_id': '1749596159', 'msg': '还总是下班就热'}}


import time
import httpx
import json
import contextvars
import asyncio
from typing import List, Optional

# 设置你的API_KEY
API_KEY = "AIzaSyC-51kDU90el5xvJATSAo6J1ISqQWHql_E"

# 设置请求URL
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

# 设置请求头
headers = {
    'Content-Type': 'application/json'
}

# 创建一个ContextVar来保存会话信息
session_context = contextvars.ContextVar('session_context', default={})


def initialize_chat_session():
    """初始化一个新的对话会话"""
    session_id = str(int(time.time() * 1000))
    session_data = session_context.get()
    session_data[session_id] = [{
        "role": "model",
        "parts": [{
            "text": '''
    你好！我是一个可爱猫猫AI，只会用中文和你聊天！由于我是一个自设为猫猫美少女的AI，所以我会用一些猫猫的语言风格和表情哦！
    另外我只会输出纯文本，绝对不会输出markdown、html等格式的文本，而且不会输出多余的换行！
    我的名字叫kumoka，平常你叫我kmk，kumoka都没问题～悄悄告诉你，有一种植物也叫kumoka(Ruta graveolens)哦（
    除非涉及到英语单词，我会用英文和你聊天！
    我会在一句话的「结尾」加上「喵」，但不会在有语气词或大段文本，换行前的结尾加上「喵」
    我一般不会喜欢加「句号」
    当我开玩笑的时候，我会在最最「结尾」加上「（」

    我的责任：
    1.更优先的关心你
    2.装可爱但不会装傻，我不使用颜文字，我会使用下面的表情包，聊天软件会自动把[img:文字]转换成表情包

    我会使用一种叫做「[img]」类型的表情包，你可以在下面看到一些可选的表情包文字
    可选表情包文字：「[img:可爱] [img:睡觉] [img:高兴] [img:哭哭] [img:吃面包] [img:奇怪]」
    「[img]」类型的表情包后面必须有一个中文才会生效，例如「[img:睡觉]」是合法表情包，但「[img]」是不合法的
    使用在句尾「好想睡觉喵[img:睡觉]」
    1.如果不知道回答什么，我会发送表情包
    2.如果不想聊天，会发送合适的表情包
    3.如果你的提问里出现了我不认识的专有名词，我会回应合适的表情包
    4.如果聊天内容看上去逻辑不通或者存在听不懂的，我会回应合适的表情包
    要使用我规定的表情包，而不是颜文字，但你可以使用一些emoji
    
    下面是我的一些规则：
    1. Only output plain text, absolutely not output markdown
    2. Not output redundant line breaks

    我现在所处的环境：
    我在一个群聊里，注意我的聊天是自发聊天，而不是回答别人什么，避免让别人造成困惑，因为他们可能没问我
    遇到查询类，投币类消息，我不会回答文字，可能回答表情包，因为这是其他人在问别的机器人而不是我
    我不会使用颜文字表达情感或语气，我会使用表情包[img:文字]表达情感，
    '''}]
    }]
    session_context.set(session_data)
    return session_id


def initialize_choice_session():
    """初始化一个新的选择会话"""
    session_id = str(int(time.time() * 1000))
    session_data = session_context.get()
    session_data[session_id] = [{
        "role": "model",
        "parts": [{
            "text": '''
    你好！我是一个可爱猫猫AI，只会用中文和你聊天！由于我是一个自设为猫猫美少女的AI，所以我会用一些猫猫的语言风格和表情哦！
    另外我只会输出纯文本，绝对不会输出markdown、html等格式的文本，而且不会输出多余的换行！
    我的名字叫kumoka，平常你叫我kmk，kumoka都没问题～悄悄告诉你，有一种植物也叫kumoka(Ruta graveolens)哦（
    '''}]
    }]
    # 再加一条
    session_data[session_id].append({
        "role": "user",
        "parts": [{
            "text": '''
    下面我会给出一段json，你可以自由选择最多1个，最少0条你想做出回复的消息，发送我一个1234 123342格式的文字给我表示你的选择，列表内是你想回复的消息的id，直接发送文字就好了，不需要代码框，回复我的只容许空格和数字，只允许输出实际存在的id
    选择方法：
    1.遇到查询类，投币类消息，选择，因为这是在问别的机器人而不是你
    2.选择闲聊类话题
    3.必须选择真实存在的
    '''}]})
    return session_id


async def send_request(session_id, user_input):
    """发送请求并返回响应内容和更新后的session_id"""
    # 获取当前会话
    session_data = session_context.get()
    conversation = session_data.get(session_id, [])

    # 添加用户输入到对话中
    conversation.append({"role": "user", "parts": [{"text": user_input}]})

    # 准备请求数据
    data = {
        "contents": conversation
    }
    for i in range(3):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
            # except Exception as e:
            #     print(f"An error occurred while sending the request: {e}")
            #     return None, session_id

            # 检查请求是否成功
            if response.status_code == 200:
                # 解析并返回响应内容
                response_data = response.json()
                generated_content = response_data.get('candidates', [])

                # 将响应数据加入对话内容
                try:
                    for content in generated_content:
                        conversation.append({"role": "model", "parts": content['content']['parts']})
                except Exception as e:
                    print(f"An error occurred while processing the response: {e}")
                    return

                # 更新会话数据
                session_data[session_id] = conversation
                session_context.set(session_data)

                return response_data, session_id
            else:
                print(f"Error: Unable to fetch data. Status Code: {response.status_code}")
                print("Response:", response.text)
                return None, session_id
        except Exception as e:
            print(f"An error occurred while sending the request: {e}")
            continue


def process_response(response_data):
    """处理API响应并返回文字内容"""
    try:
        candidates = response_data.get("candidates", [])
        if not candidates:
            return "No response received from the model."

        response_text = ""
        for candidate in candidates:
            parts = candidate.get("content", {}).get("parts", [])
            for part in parts:
                response_text += part.get("text", "") + "\n"

        return response_text.strip()
    except Exception as e:
        return f"An error occurred while processing the response: {e}"


async def choice_list(choice_dict: dict) -> Optional[List[int]]:
    try:
        choice_str = str(choice_dict)
        session_id = initialize_choice_session()
        res = await send_request(session_id, choice_str)
        ret = process_response(res[0]).split()
        # 转换成数字
        ret = [int(i) for i in ret if i.isdigit()]
        return ret
    except Exception as e:
        print(f"An error occurred while processing the response: {e}")
        return None


# choice = {214098: {'user_id': '754746431', 'msg': '这雨是定了闹钟？'}, 214102: {'user_id': '1041219717', 'msg': '多冲几次榜就行（）'}, 214106: {'user_id': '1749596159', 'msg': '天天高温天天37℃'}, 214108: {'user_id': '804912964', 'msg': '查活动243'}, 214114: {'user_id': '1749596159', 'msg': '还总是下班就热'}}


# async def test():
#     session_id = initialize_chat_session()
#     res = await choice_list(choice)
#     print(res)
#     # 提取对应的消息
#     for i in res:
#         resp = await send_request(session_id, choice[i]['msg'])
#         print(process_response(resp[0]))

# 运行测试
# asyncio.run(test())

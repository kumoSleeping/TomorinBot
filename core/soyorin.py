import json
import os
import yaml
import re
import time
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from rana import Session


'''
Soyorin.py
消息审核 / 插件管理 / 黑白名单 API
与 ./plugin 界限模糊，类似服务组件 API
'''

ban_dicts_path = './plugins/soyorin/ban_dicts.json'
ADMINISTRATOR_list = ['1528593481']
config: dict = yaml.safe_load(open('config.yml', encoding='utf-8'))


class BanManager:
    ALL_BAN_DICTS: List[Dict] = []

    @classmethod
    def load_data(cls):
        global ban_dicts_path
        if os.path.exists(ban_dicts_path):
            with open(ban_dicts_path, 'r', encoding='utf-8') as file:
                cls.ALL_BAN_DICTS = json.load(file)
        else:
            cls.ALL_BAN_DICTS = []

    @classmethod
    def save_data(cls):
        global ban_dicts_path
        with open(ban_dicts_path, 'w', encoding='utf-8') as file:
            json.dump(cls.ALL_BAN_DICTS, file, ensure_ascii=False, indent=4)

    @classmethod
    def add_item(cls, item):
        cls.ALL_BAN_DICTS.append(item)
        BanManager.save_data()

    @classmethod
    def delete_item(cls, index):
        if 0 <= index < len(cls.ALL_BAN_DICTS):
            del cls.ALL_BAN_DICTS[index]
            BanManager.save_data()
        else:
            print("索引超出范围")

    @staticmethod
    def check_before_plugin(session: "Session", plugin_name: str):
        # print(BanManager.ALL_BAN_DICTS)
        for ban_config in BanManager.ALL_BAN_DICTS:
            if plugin_name == 'soyorin':
                return True
            # 初始化变量
            guild_ = ban_config.get('G', ban_config.get('G', 'N/A'))
            platform_ = ban_config.get('P', ban_config.get('P', 'N/A'))
            user_ = ban_config.get('U', ban_config.get('U', 'N/A'))
            func_ = ban_config.get('F', ban_config.get('F', 'N/A'))
            message_ = ban_config.get('M', ban_config.get('M', 'N/A'))

            if guild_ != session.guild.id and guild_ != 'N/A':
                continue
            if platform_ != session.platform and platform_ != 'N/A':
                continue
            if user_ != session.user.id and user_ != 'N/A':
                continue
            if func_ != plugin_name and func_ != 'N/A':
                continue
            if message_ != session.message and message_ != 'N/A':
                continue
            # print("不通过")
            return False  # 此消息审核 不过
        # print('通过')
        return True  # 此消息审核 过


BanManager.load_data()


class Utils:
    @staticmethod
    def escape_special_characters(message: str):
        # 替换特殊字符为转义字符
        message = message.replace('&', '&amp;')
        message = message.replace('"', '&quot;')
        message = message.replace('<', '&lt;')
        message = message.replace('>', '&gt;')
        return message

    @staticmethod
    def unescape_special_characters(escaped_message: str):
        # 将转义字符替换回特殊字符
        escaped_message = escaped_message.replace('&quot;', '"')
        escaped_message = escaped_message.replace('&amp;', '&')
        escaped_message = escaped_message.replace('&lt;', '<')
        escaped_message = escaped_message.replace('&gt;', '>')
        return escaped_message

    @staticmethod
    def show_session_log(session: "Session"):
        # 展示日志
        message_content = session.message.content

        html_tag_pattern = re.compile(r'<.*?>')
        # 将所有HTML标签替换为占位符
        cleaned_text = re.sub(html_tag_pattern, '[xml元素]', message_content)
        cleaned_text = cleaned_text[0:15] + '...' if len(cleaned_text) > 15 else cleaned_text
        cleaned_text = cleaned_text.replace("\n", " ").replace("\r", " ")
        user_id = session.user.id

        member = session.user.name
        if not member:
            # 为什么是QQ用户，因为就QQ可能拿不到成员name...
            member = f'用户{user_id}'

        try:
            group = session.guild.name
            if not group:
                group = f'频道: {session.channel.name}'
        except:
            # 为什么是QQ用户，因为就QQ可能拿不到成员name...
            group = f'用户{user_id}'

        print(f"[ {session.platform}: {group} ] （ {member} ）{cleaned_text}")


class Queue:
    rpl_queue: List[Dict] = []

    @staticmethod
    def add(time_int: int, message: str, self_id: str):
        global rpl_queue
        connections = config["connections"]
        for connection_config in connections:
            if connection_config["link_way"] == 'only_webhook':
                if self_id in connection_config["self_ids"]:
                    data_rpl_queue = {"timestamp": time_int, "message": message}
                    Queue.rpl_queue.append(data_rpl_queue)
                    print('插入消息池成功')
                    # 设置等待的最大时间（以秒为单位）
                    max_wait_time = connection_config['life_cycle']

                    # 记录开始时间
                    for item in Queue.rpl_queue:
                        if time_int - item["timestamp"] > max_wait_time * 1000:
                            Queue.rpl_queue.remove(item)
                            print('删除超时玩意')
                    break







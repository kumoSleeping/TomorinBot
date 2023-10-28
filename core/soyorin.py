import json
import os
import yaml
import re

'''
Soyorin.py
消息审核 / 插件管理 / 黑白名单 API
与 ./plugin 界限模糊，类似服务组件 API
'''


ban_dicts_path = './plugins/soyorin/ban_dicts.json'
config = yaml.safe_load(open('config.yml', encoding='utf-8'))
ADMINISTRATOR_list = ['1528593481']


class BanManager:
    ALL_BAN_DICTS = []

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
    def check_before_plugin(session, plugin_name):
        # print(BanManager.ALL_BAN_DICTS)
        for idx, ban_config in enumerate(BanManager.ALL_BAN_DICTS):
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
    def escape_special_characters(message):
        # 替换特殊字符为转义字符
        message = message.replace('&', '&amp;')
        message = message.replace('"', '&quot;')
        message = message.replace('<', '&lt;')
        message = message.replace('>', '&gt;')
        return message

    @staticmethod
    def unescape_special_characters(escaped_message):
        # 将转义字符替换回特殊字符
        escaped_message = escaped_message.replace('&quot;', '"')
        escaped_message = escaped_message.replace('&amp;', '&')
        escaped_message = escaped_message.replace('&lt;', '<')
        escaped_message = escaped_message.replace('&gt;', '>')
        return escaped_message

    @staticmethod
    def show_session_log(session):
        # 展示日志
        message_content = session.message.content

        html_tag_pattern = re.compile(r'<.*?>')
        # 将所有HTML标签替换为占位符
        cleaned_text = re.sub(html_tag_pattern, '[xml元素]', message_content)
        cleaned_text = cleaned_text[0:15] + '...' if len(cleaned_text) > 15 else cleaned_text
        cleaned_text = cleaned_text.replace("\n", " ").replace("\r", " ")
        user_id = session.user.id
        try:
            member = session.user.name
            if not member:
                member = f'QQ用户{user_id}'
        except:
            # 为什么是QQ用户，因为就QQ可能拿不到成员name...
            member = f'QQ用户{user_id}'

        try:
            group = session.guild.name
            if not group:
                group = f'频道: {session.channel.name}'
        except:
            # 为什么是QQ用户，因为就QQ可能拿不到成员name...
            group = f'QQ用户{user_id}'

        print(f"[ {session.platform}: {group} ] （ {member} ）{cleaned_text}")





import json
import os,\
    inspect,\
    yaml
import re

config = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yml')))

IP, PORT, TOKEN, Heartbeat_cd, ADMINISTRATOR_list = config['server']["ip"], config['server']["port"],\
    config['server']["token"], config['server']["HeartbeatInterval"], config['user']["administrator"]

'''
Soyorin.py
消息审核 / 插件管理 / 黑白名单 API
与 ./plugin 界限模糊，类似服务组件 API
'''


# file_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/plugin_package/_plugin_data/_soyorin/ban_dicts.json'
# print(file_path)
relative_path = 'plugin_package/_plugin_data/_soyorin/ban_dicts.json'

# 获取当前脚本所在目录的绝对路径
script_directory = os.path.dirname(os.path.abspath(__file__))

# 获取父目录（上一级目录）的绝对路径
parent_directory = os.path.dirname(script_directory)

# 拼接相对路径和父目录的绝对路径
file_path = os.path.join(parent_directory, relative_path)

print(file_path)


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


class BanManager:
    ALL_BAN_DICTS = []
    @classmethod
    def load_data(cls):
        global file_path
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                cls.ALL_BAN_DICTS = json.load(file)
        else:
            cls.ALL_BAN_DICTS = []

    @classmethod
    def save_data(cls):
        global file_path
        with open(file_path, 'w', encoding='utf-8') as file:
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
            if plugin_name == '_soyorin':
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
# print(BanManager.ALL_BAN_DICTS)
print('服务[BanManager]加载成功！\nSoyorin.py 导入服务结束')
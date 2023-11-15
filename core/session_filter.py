import json
import os
from typing import List, Dict, TYPE_CHECKING

from config import ban_dicts_path


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
ban_manager = BanManager




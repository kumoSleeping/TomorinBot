import json
import os
from typing import List, Dict, TYPE_CHECKING
from core import event, Event, on
from core.loader import config

from plugins.action import Action
from plugins.auth import is_admin

ban_dicts_path = 'plugins/event_filter/ban_dicts.json'


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
    def check_before_plugin(event: Event, plugin_name: str):
        # print(BanManager.ALL_BAN_DICTS)
        for ban_config in BanManager.ALL_BAN_DICTS:
            # print(ban_config)
            # print(plugin_name)
            if plugin_name == 'soyorin':
                return True
            # 初始化变量
            guild_ = ban_config.get('G', ban_config.get('G', 'N/A'))
            platform_ = ban_config.get('P', ban_config.get('P', 'N/A'))
            user_ = ban_config.get('U', ban_config.get('U', 'N/A'))
            func_ = ban_config.get('F', ban_config.get('F', 'N/A'))
            message_ = ban_config.get('M', ban_config.get('M', 'N/A'))

            if guild_ != event.guild.id and guild_ != 'N/A':
                continue
            if platform_ != event.platform and platform_ != 'N/A':
                continue
            if user_ != event.user.id and user_ != 'N/A':
                continue
            if func_ != plugin_name and func_ != 'N/A':
                continue
            if message_ != event.message and message_ != 'N/A':
                continue
            # print("不通过")
            return False  # 此消息审核 不过
        # print('通过')
        return True  # 此消息审核 过


if not os.path.exists(ban_dicts_path):
    with open(ban_dicts_path, 'w', encoding='utf-8') as file:
        json.dump([], file, ensure_ascii=False, indent=4)
BanManager.load_data()
ban_manager = BanManager


@on.before_plugin_do
def soyo0(event: Event, plugin: callable):
    plugin_name = plugin.__name__
    if not ban_manager.check_before_plugin(event, plugin_name):
        # print(f'[filter] ID 为 {event.message.id} 的消息被过滤')
        return event, None
    return event, plugin


@on.message_created
def _soyo1(event: Event):
    action = Action(event)
    action.description = 'soyo0黑名单管理插件'
    action.command(['ign'], ign)
    action.command(['-ign'], _ign)


def ign(action):
    if action.args:
        if is_admin(action.event.platform, action.event.user.id):
            print('[!] 权限不足～')
            return
        ele_list = action.args

        replacement_values = {'G': action.event.guild.id, 'U': 'Default', 'P': action.event.platform,
                              'M': action.event.message.content, 'F': 'Default'}
        ban_dict = {part[0]: part[1:] if part[1:] else replacement_values.get(part[0], 'Default') for part in
                    ele_list if part[0] in replacement_values}

        BanManager.add_item(ban_dict)
        action.send(f'已执行·添加逻辑成功')
    else:
        output_lines = []
        for i, ban_dict in enumerate(BanManager.ALL_BAN_DICTS, start=0):
            output_line = f"Item {i}: "
            output_line += ', '.join([f"{key}: {value}" for key, value in ban_dict.items()])
            output_lines.append(output_line)

        rpl = '\n'.join(output_lines)
        action.send(f'<at id="{action.event.user.id}"/> 目前支持的保留字有: G、U、P、M、F\n分别表示 Guild User Message Platform Func\n目前的逻辑列表为:\n{rpl}')
        return


def _ign(action):

    # 按照顺序移除忽略
    if action.args:
        if is_admin(action.event.platform, action.event.user.id):
            print('[!] 权限不足～')
            return
        item_index = int(action.text)
        BanManager.delete_item(item_index)
        action.send(f'已执行·删除逻辑 [item {item_index}]')


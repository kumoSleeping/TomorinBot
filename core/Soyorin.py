import json
import os
import copy
import inspect


'''
Soyorin.py
消息审核 / 插件管理 / 黑白名单 API
与 ./plugin 界限模糊，类似服务组件 API
'''

ALL_BAN_DICTS = []

file_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/utils/ban_dicts.json'

if os.path.exists(file_path):
    # 如果文件存在，读取已有内容
    with open(file_path, 'r', encoding='utf-8') as file:
        ALL_BAN_DICTS = json.load(file)
else:
    ALL_BAN_DICTS = []


class Soyorin:
    @staticmethod
    def save_ban_config(ban_dict):
        """
        Save ban_dict to the specified JSON file and append it to the large dictionary.
        保存 ban_dict 到指定的 JSON 文件，并追加到大字典中。
        """
        global ALL_BAN_DICTS

        # 将 ban_dict 追加到大字典中
        ALL_BAN_DICTS.append(copy.deepcopy(ban_dict))

        # 保存到文件
        with open(file_path, 'w', encoding='utf-8') as file:
            # 将所有 ban_dict 写入文件
            json.dump(ALL_BAN_DICTS, file, ensure_ascii=False, indent=4)

    @staticmethod
    def delete_ban_config(index_to_delete):
        global ALL_BAN_DICTS

        def delete_ban_dict(index_to_delete):
            """
            Deletes the element at the specified index in the list.
            删除列表中指定索引处的元素。

            """
            if 0 <= index_to_delete < len(ALL_BAN_DICTS):
                del ALL_BAN_DICTS[index_to_delete]
            else:
                print("你好，索引超了")

            return ALL_BAN_DICTS

        ALL_BAN_DICTS = delete_ban_dict(index_to_delete)
        # 保存到文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(ALL_BAN_DICTS, file, ensure_ascii=False, indent=4)
        return

    @staticmethod
    def check_before_plugin(session, plugin_name):
        '''

        :param session:
        :return:
        '''

        for idx, ban_config in enumerate(ALL_BAN_DICTS):
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

            return False  # 此消息审核 不过
        return True  # 此消息审核 过

    @staticmethod
    def check_before_send(session):
        '''

        :param session:
        :return:
        '''

        return True






import json
import os
import copy
from server import current_file_directory

'''
Soyorin.py
消息审核 / 插件管理 / 黑白名单 API
与 ./plugin 界限模糊，类似服务组件 API
'''

file_path = current_file_directory + '/core/utils/ban_dicts.json'
if os.path.exists(file_path):
    # 如果文件存在，读取已有内容
    with open(file_path, 'r', encoding='utf-8') as file:
        all_ban_dicts = json.load(file)
else:
    all_ban_dicts = []


def save_ban_dict_to_file(ban_dict):
    """
    Save ban_dict to the specified JSON file and append it to the large dictionary.
    保存 ban_dict 到指定的 JSON 文件，并追加到大字典中。
    """
    global all_ban_dicts

    # 将 ban_dict 追加到大字典中
    all_ban_dicts.append(copy.deepcopy(ban_dict))

    # 保存到文件
    with open(file_path, 'w', encoding='utf-8') as file:
        # 将所有 ban_dict 写入文件
        json.dump(all_ban_dicts, file, ensure_ascii=False, indent=4)


def delete_ban_dict_item(index_to_delete):
    global all_ban_dicts

    def delete_ban_dict(index_to_delete):
        """
        Deletes the element at the specified index in the list.
        删除列表中指定索引处的元素。

        """
        if 0 <= index_to_delete < len(all_ban_dicts):
            del all_ban_dicts[index_to_delete]
        else:
            print("你好，索引超了")

        return all_ban_dicts

    all_ban_dicts = delete_ban_dict(index_to_delete)
    # 保存到文件
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(all_ban_dicts, file, ensure_ascii=False, indent=4)
    return


def check_before_plugin(session, plugin_name):
    '''

    :param session:
    :return:
    '''

    for idx, ban_config in enumerate(all_ban_dicts):
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


def check_before_send(session):
    '''

    :param session:
    :return:
    '''

    return True






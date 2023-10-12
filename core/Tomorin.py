import json
import re
from .Rana import process_satori_message
from .Rikki import send, send_message
from .Soyorin import check_before_plugin, check_before_send, save_ban_dict_to_file, all_ban_dicts, delete_ban_dict_item
from server import administrator
'''
Tmorin.py
处理所有插件
核心处理调度 data 和 发送
'''

plugin_configurations = []


def plugin(func):
    print(f'插件[{str(func).split()[1]}]加载成功')
    plugin_configurations.append(func)


def Main(data):
    session = process_satori_message(data)
    # 插件管理 / 黑名单审查

    for plugin in plugin_configurations:
        if not check_before_plugin(session, str(plugin).split()[1]):
            print('[WARNING] 消息被soyorin拦截...')
            continue
        plugin(session)


@plugin
def hello(session):
    if session.message.content == '你好':
        send(f'你好喵（ <at id="{session.user.id}"/>', session)


@plugin
def photo_(session):
    if session.message.content == '喵喵':
        send(f'<at id="{session.user.id}"/> 喵喵', session)



from .plugin.tsugu.tsuguLP import tsugu_main

@plugin
def tsugulp(session):
    if not session.message.content:
        return
    rpl = tsugu_main(session.message.content, session.user.id, session.guild.id)
    if not rpl:
        pass
    else:
        modified_results = []
        for item in rpl:
            if item['type'] == 'string':
                # 处理字符串类型的结果，可能是文本消息
                text_message = item['string']
                modified_results.append(text_message)
            elif item['type'] == 'base64':
                # 处理Base64编码的图像数据
                base64_data = item['string']
                # 将Base64数据包裹在^IMG=xxx^中并添加到文本中
                image_tag = f'^[图片:等satori支持发图]^'
                modified_results.append(image_tag)
        result_string = ''.join(modified_results)
        send(result_string, session)


@plugin
def _soyorin(session):
    if session.message.content.strip() == 'ign':
        send(f'<at id="{session.user.id}"/> 目前支持的保留字有: G、U、P、M、F\n分别表示 Guild User Message Platform Func',
             session)
        return
    # 忽略
    if session.message.content.startswith('ign '):
        if session.user.id not in administrator:
            print('[!] 权限不足～')
            return
        ele_list = session.message.content.strip().split()

        replacement_values = {'G': session.guild.id, 'U': 'Default', 'P': session.platform,
                              'M': session.message.content, 'F': 'Default'}
        ban_dict = {part[0]: part[1:] if part[1:] else replacement_values.get(part[0], 'Default') for part in
                    ele_list if part[0] in replacement_values}

        save_ban_dict_to_file(ban_dict)
        # send(f'<at id="{session.user.id}"/> 喵喵，ban_dict测试结果为{str(ban_dict)}', session)

    # 按顺序展示忽略了哪些
    if session.message.content.startswith('ignwhat'):
        output_lines = []
        for i, ban_dict in enumerate(all_ban_dicts, start=0):
            output_line = f"Item {i}: "
            output_line += ', '.join([f"{key}: {value}" for key, value in ban_dict.items()])
            output_lines.append(output_line)

        rpl = '\n'.join(output_lines)
        send(rpl, session)

    # 按照顺序移除忽略
    if session.message.content.startswith('-ign'):

        if session.user.id not in administrator:
            print('[!] 权限不足～')
            return
        item_index = session.message.content.replace("-ign", "").strip()
        item_index = int(item_index)
        delete_ban_dict_item(item_index)


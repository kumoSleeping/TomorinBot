from core.Rana import Rana, h
from core.Rikki import Rikki, send
from core.Soyorin import BanManager
from core.Soyorin import ADMINISTRATOR_list

from PIL import Image

plugin_configurations = []


def plugin(func):
    print(f'插件[{str(func).split()[1]}]加载成功！')
    plugin_configurations.append(func)


@plugin
def hello(session):
    if session.message.content == '测试音频':
        send(f'{h.audio_url("https://bestdori.com/assets/jp/sound/bgm542_rip/bgm542.mp3")}', session)


@plugin
def test(session):
    if session.message.content == '测试':
        image = Image.new('RGB', (50, 50), color='red')
        send(f'{h.quote(session.message.id)} {h.at(session.user.id)} 爱城华恋色图：{h.image_pil(image)}', session)


# from plugin_package._plugin_data.zmngu import get_result
#
# @plugin
# def tsugulp(session):
#     if not session.message.content:
#         return
#     rpl = get_result(session.message.content, session.user.id, session.guild.id)
#     if not rpl:
#         pass
#     else:
#         modified_results = []
#         for item in rpl:
#             if item['type'] == 'string':
#                 # 处理字符串类型的结果，可能是文本消息
#                 text_message = item['string']
#                 modified_results.append(text_message)
#             elif item['type'] == 'base64':
#                 # 处理Base64编码的图像数据
#                 base64_data = item['string']
#                 # 将Base64数据包裹在^IMG=xxx^中并添加到文本中
#                 image_tag = f''
#                 modified_results.append(image_tag)
#         result_string = ''.join(modified_results)
#         send(result_string, session)


@plugin
def _soyorin(session):
    if session.message.content.strip() == 'ign':
        send(f'<at id="{session.user.id}"/> 目前支持的保留字有: G、U、P、M、F\n分别表示 Guild User Message Platform Func',
             session)
        return
    # 忽略
    if session.message.content.startswith('ign '):
        if session.user.id not in ADMINISTRATOR_list:
            print('[!] 权限不足～')
            return
        ele_list = session.message.content.strip().split()

        replacement_values = {'G': session.guild.id, 'U': 'Default', 'P': session.platform,
                              'M': session.message.content, 'F': 'Default'}
        ban_dict = {part[0]: part[1:] if part[1:] else replacement_values.get(part[0], 'Default') for part in
                    ele_list if part[0] in replacement_values}

        BanManager.add_item(ban_dict)
        # send(f'<at id="{session.user.id}"/> 喵喵，ban_dict测试结果为{str(ban_dict)}', session)

    # 按顺序展示忽略了哪些
    if session.message.content.startswith('ignwhat'):
        output_lines = []
        for i, ban_dict in enumerate(BanManager.ALL_BAN_DICTS, start=0):
            output_line = f"Item {i}: "
            output_line += ', '.join([f"{key}: {value}" for key, value in ban_dict.items()])
            output_lines.append(output_line)

        rpl = '\n'.join(output_lines)
        send(rpl, session)

    # 按照顺序移除忽略
    if session.message.content.startswith('-ign'):

        if session.user.id not in ADMINISTRATOR_list:
            print('[!] 权限不足～')
            return
        item_index = session.message.content.replace("-ign", "").strip()
        item_index = int(item_index)
        BanManager.delete_item(item_index)


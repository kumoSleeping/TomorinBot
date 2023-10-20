from PIL import Image
from pathlib import Path

from core.Rana import h
from core.Rikki import bot
from core.Soyorin import BanManager
from core.Soyorin import ADMINISTRATOR_list

component_configurations = []


def component(func):
    print(f'组件[{str(func).split()[1]}]加载成功！')
    component_configurations.append(func)


@component
def test1(session):
    if session.message.content == '测试文字':
        session.send('测试成功！')


@component
def test2(session):
    if session.message.content == '测试音频':
        session.send(f'{h.audio("https://bestdori.com/assets/jp/sound/bgm542_rip/bgm542.mp3")}')


@component
def test3(session):
    if session.message.content == '测试混合元素':
        image = Image.new('RGB', (50, 50), color='red')
        # h.image(image) 可以直接通过传 PIL 对象发送图片
        session.send(f'{h.quote(session.message.id)} {h.at(session.user.id)} 爱城华恋色图：{h.image(image)}')


@component
def test4(session):
    if session.message.content.startswith('发送到群组'):
        forward_guild_id: str = session.message.content[5:].strip()
        rpl = bot.send(f'这是一条来自 {session.guild.name} 的消息', session.platform, forward_guild_id, session.self_id)
        if not rpl:
            session.send(f"发送失败")
        else:
            session.send('发送成功')


# 随便规范 _开头表示 框架内置插件 也可以不用
@component
def _soyorin(session):
    if session.message.content.strip() == 'ign':
        session.send(f'<at id="{session.user.id}"/> 目前支持的保留字有: G、U、P、M、F\n分别表示 Guild User Message Platform Func')
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
        session.send(rpl)

    # 按照顺序移除忽略
    if session.message.content.startswith('-ign'):

        if session.user.id not in ADMINISTRATOR_list:
            print('[!] 权限不足～')
            return
        item_index = session.message.content.replace("-ign", "").strip()
        item_index = int(item_index)
        BanManager.delete_item(item_index)













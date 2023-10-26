import importlib


def soyorin(session):
    '''
    黑白名单总揽管理
    '''
    # 动态导入模块
    module = importlib.import_module("core.soyorin")
    # 访问模块中的 function_info_list
    BanManager, ADMINISTRATOR_list = module.BanManager, module.ADMINISTRATOR_list

    if session.message.content.strip() == 'ign':
        output_lines = []
        for i, ban_dict in enumerate(BanManager.ALL_BAN_DICTS, start=0):
            output_line = f"Item {i}: "
            output_line += ', '.join([f"{key}: {value}" for key, value in ban_dict.items()])
            output_lines.append(output_line)

        rpl = '\n'.join(output_lines)
        session.send(f'<at id="{session.user.id}"/> 目前支持的保留字有: G、U、P、M、F\n分别表示 Guild User Message Platform Func\n目前的逻辑列表为:\n{rpl}')
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
        session.send(f'已执行·添加逻辑成功')
        # send(f'<at id="{session.user.id}"/> 喵喵，ban_dict测试结果为{str(ban_dict)}', session)

    # 按照顺序移除忽略
    if session.message.content.startswith('-ign'):

        if session.user.id not in ADMINISTRATOR_list:
            print('[!] 权限不足～')
            return
        item_index = session.message.content.replace("-ign", "").strip()
        item_index = int(item_index)
        BanManager.delete_item(item_index)

        session.send(f'已执行·删除逻辑 [item {item_index}]')







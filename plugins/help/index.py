import importlib


def help(session):
    """
    help组件
    发送help查看帮助。
    """

    import os
    import inspect
    import sys

    def load_function_info_list():
        function_info_list = []
        for folder in [d for d in os.listdir('./plugins')
                       if os.path.isdir(os.path.join('./plugins', d)) and not d.startswith('__')]:
            folder_info = {'folder_name': folder, 'functions': []}

            module = importlib.import_module(f'plugins.{folder}.index')
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and not name.startswith(
                        '_') and obj.__module__ == f'plugins.{folder}.index':  # 添加过滤条件

                    function_info = {
                        'function_name': name,
                        'function_docstring': inspect.getdoc(obj)
                    }
                    folder_info['functions'].append(function_info)

                    function_info_list.append(function_info)
        return function_info_list

    def get_text_before_first_newline(text):
        # 查找第一个换行符的索引
        first_newline_index = text.find('\n')

        if first_newline_index != -1:
            # 截取第一个换行符之前的文本
            result = text[:first_newline_index]
        else:
            # 如果没有找到换行符，返回整个文本
            result = text

        return result

    if session.message.content in ['helb', 'help']:
        help_list = ""  # 初始化一个空字符串
        function_info_list = load_function_info_list()

        for item in function_info_list:
            function_name = item['function_name']
            function_docstring = item['function_docstring']

            if not function_docstring:
                function_docstring = ''

            if function_name and function_docstring:
                help_list += f"  {function_name}  {get_text_before_first_newline(function_docstring)}\n"
        help_list = help_list[:-2]
        rpl = f'''当前可用的组件有：
{help_list}
输入“help指令名”查看组件作者写了啥玩意。'''
        session.send(rpl)

    if str(session.message.content).startswith('helb ') or str(session.message.content).startswith('help '):
        # print(function_info_list)
        search_value = session.message.content[5:]
        function_info_list = load_function_info_list()


        found_docstring = None

        for item in function_info_list:
            if item['function_name'] == search_value:
                docstring = item['function_docstring']
                if docstring is not None:
                    found_docstring = docstring
                    break
            if found_docstring:
                break  # 如果找到匹配项，就退出外层循环

        if found_docstring is not None:
            found_docstring = found_docstring.replace('\n', '\n  ')
            session.send(found_docstring)







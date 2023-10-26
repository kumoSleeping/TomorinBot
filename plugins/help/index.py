import importlib


def help(session):
    """
    help组件
    发送help查看帮助。
    """
    # 动态导入模块
    module = importlib.import_module("core.tomorin")
    # 访问模块中的 function_info_list
    function_info_list = module.function_info_list

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

        for item in function_info_list:
            for function in item['functions']:
                function_name = function['function_name']
                function_docstring = function['function_docstring']

                if not function_docstring:
                    function_docstring = ''

                if function_name and function_docstring:
                    help_list += f"  {function_name}  {get_text_before_first_newline(function_docstring)}\n"
        help_list = help_list[:-2]
        rpl = f'''当前可用的指令有：
{help_list}
输入“help指令名”查看插件作者写了啥玩意。'''
        session.send(rpl)

    if str(session.message.content).startswith('helb ') or str(session.message.content).startswith('help '):
        search_value = session.message.content[5:]
        # print(function_info_list)

        found_docstring = None

        for item in function_info_list:
            for function in item['functions']:
                if function['function_name'] == search_value:
                    docstring = function['function_docstring']
                    if docstring is not None:
                        found_docstring = docstring
                        break
            if found_docstring:
                break  # 如果找到匹配项，就退出外层循环

        if found_docstring is not None:
            session.send(found_docstring)







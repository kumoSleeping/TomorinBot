import importlib
import os
import inspect
from core.load_plugins import data_nil
from bridge.session_adder import SessionExtension

from bridge.tomorin import on_activator, on_event


def load_function_info_list():
    function_info_list = []
    for folder in [d for d in os.listdir('./plugins')
                   if os.path.isdir(os.path.join('./plugins', d)) and not d.startswith('__')]:
        folder_info = {'folder_name': folder, 'functions': []}

        module = importlib.import_module(f'plugins.{folder}.index')
        for name, obj in inspect.getmembers(module):
            if not (
                    inspect.isfunction(obj) and
                    # not name.startswith('_') and
                    obj.__module__ == f'plugins.{folder}.index' and
                    len(inspect.signature(obj).parameters) != 0
                    # and inspect.getdoc(obj) is not None

            ):
                continue
            # 这个语句是为了在「不是插件的函数」传递「session」时抛出异常时结束这本次导入
            session_nil = SessionExtension(data_nil)
            try:
                obj(session_nil)
            except:
                continue
            if not hasattr(obj, 'enable_feature'):
                continue
            # self.loaded_plugins[name] = obj
            # print(f'[load_plugins] [{folder}] 加载插件 [{obj.__name__}]')
            name = obj.__name__

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


@on_activator.command(['help', '帮助'])
def help(session):
    """
    help组件
    发送help查看帮助。
    """
    help_list = ""  # 初始化一个空字符串
    for item in load_function_info_list():
        function_name, function_docstring = item['function_name'], item['function_docstring']
        function_docstring = '' if not function_docstring else function_docstring
        if function_name and function_docstring:
            help_list += f"  .{function_name}  {get_text_before_first_newline(function_docstring)}\n"
    help_list = help_list[:-1]
    rpl = f'''发送.组件名查询提示
{help_list}'''
    session.send(rpl)
    return


@on_event.message_created
def qwe(session):
    if str(session.message.content).startswith('.') or str(session.message.content).startswith('help '):
        search_value = str(session.message.content).replace(".", '').replace("help ", '')
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







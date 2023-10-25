import os
import importlib

from Rana import Rana
import inspect

'''
Tmorin.py
处理所有插件
核心处理调度 data 和 发送
'''


# 获取目标包下的所有文件夹
subdirectories = [d for d in os.listdir('../_plugins')
                  if os.path.isdir(os.path.join('../_plugins', d)) and not d.startswith('_')]
formatted_subdirectories = ['插件包[' + folder + ']加载成功！' for folder in subdirectories]

notice = '\n'.join(formatted_subdirectories)


def show_load_plugin():
    print(notice)


function_info_list = []

for folder in subdirectories:
    folder_info = {'folder_name': folder, 'functions': []}

    try:
        module = importlib.import_module(f'_plugins.{folder}.index')

        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith('_'):  # 添加过滤条件
                function_info = {
                    'function_name': name,
                    'function_docstring': inspect.getdoc(obj)
                }
                folder_info['functions'].append(function_info)

    except ImportError as e:
        print(f"Failed to import module {folder}: {str(e)}")
    except AttributeError as e:
        print(f"插件包 {folder} 函数或内部发生错误. \nerror: {e}")

    function_info_list.append(folder_info)
# print(function_info_list)


def main(data):
    session = Rana.process_satori_message(data)
    # 插件管理 / 黑名单审查
    # 动态导入模块
    module = importlib.import_module("core.Soyorin")
    # 访问模块中的 function_info_list
    BanManager = module.BanManager

    for folder_info in function_info_list:
        folder_name = folder_info['folder_name']
        functions = folder_info['functions']

        try:
            module = importlib.import_module(f'_plugins.{folder_name}.index')

            for function_info in functions:
                function_name = function_info['function_name']
                function_docstring = function_info['function_docstring']
                # print(function_name)
                if not BanManager.check_before_plugin(session, function_name):
                    # print('[WARNING] 消息被soyorin拦截...')
                    continue

                # 调用函数
                func = getattr(module, function_name)
                func(session)

        except ImportError as e:
            print(f"Failed to import module {folder_name}: {str(e)}")
        except AttributeError as e:
            print(f"插件包 {folder_name} 函数或内部发生错误. \nerror: {e}")






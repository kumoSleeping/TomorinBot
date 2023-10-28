import importlib
import inspect
import os

from rana import Rana


'''
Tmorin.py
处理所有插件
核心处理调度 data 和 发送
'''

function_info_list = []


def main(data):
    # print(function_info_list)
    session = Rana.process_satori_message(data)
    module = importlib.import_module("soyorin")
    # 访问模块中的 function_info_list
    ban_manager = module.BanManager

    def load_and_execute_plugins(session, folder, ban_manager):
        try:
            module = importlib.import_module(f'plugins.{folder}.index')
            for name, obj in inspect.getmembers(module):
                # 1.如果是函数 # 2.并且不以'_'开头# 3.并且函数存在于index.py而非别的文件导入进去的  # 4.并且通过了soyorin的拦截
                if (inspect.isfunction(obj) and not name.startswith('_') and obj.__module__ == f'plugins.{folder}.index') and ban_manager.check_before_plugin(session, name):
                    # 满足上面4个条件，就调用插件函数，传递 session 数据
                    obj(session)

        except ImportError as e:
            print(f"Failed to import module {folder}: {str(e)}")
        except AttributeError as e:
            print(f"插件包 {folder} 函数或内部发生错误. \nerror: {e}")

    # 主要是给help用的
    for folder in [d for d in os.listdir('./plugins') if os.path.isdir(os.path.join('./plugins', d)) and not d.startswith('__')]:
        load_and_execute_plugins(session, folder, ban_manager)



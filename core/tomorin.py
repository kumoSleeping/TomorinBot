import importlib
import inspect
import sys
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
    module = importlib.import_module("core.soyorin")
    # 访问模块中的 function_info_list
    BanManager = module.BanManager

    # 主要是给help用的
    for folder in [d for d in os.listdir('../plugins')
                   if os.path.isdir(os.path.join('../plugins', d)) and not d.startswith('__')]:
        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本的目录路
            script_directory = os.path.dirname(script_directory)  # 获取上一级目录的绝对路径
            core_directory = os.path.join(script_directory, 'core')  # 转到./core
            os.chdir(core_directory)  # 切换到这个目录
            sys.path.append(script_directory)

            module = importlib.import_module(f'plugins.{folder}.index')
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and not name.startswith('_') and obj.__module__ == f'plugins.{folder}.index':  # 添加过滤条件
                    if not BanManager.check_before_plugin(session, name):
                        # print('[WARNING] 消息被soyorin拦截...')
                        continue
                    obj(session)  # 调用插件函数，传递 session 数据

        except ImportError as e:
            print(f"Failed to import module {folder}: {str(e)}")
        except AttributeError as e:
            print(f"插件包 {folder} 函数或内部发生错误. \nerror: {e}")


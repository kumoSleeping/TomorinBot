import importlib
import inspect
import os
import threading

from session_maker import EventToSession
from session_filter import ban_manager
from session_utils import show_session_log, show_session_data


'''
处理所有插件
核心处理调度 data 和 发送
'''

function_info_list = []


def main(data):
    # 展示data
    # show_session_data(data)
    session = EventToSession.process_satori_message(data)
    # 控制台输出
    try:
        show_session_log(session)
        pass
    except Exception as e:
        print(f'[Error] Rana 抛出 {e}')
    # 访问模块中的 function_info_list

    def execute_plugin(session, obj):
        if ban_manager.check_before_plugin(session, obj.__name__):
            # 满足拦截条件，就调用插件函数，传递 session 数据
            obj(session)

    def load_and_execute_plugins(session, folder):
        module = importlib.import_module(f'plugins.{folder}.index')
        for name, obj in inspect.getmembers(module):
            # 1. 如果是函数
            # 2. 并且不以'_'开头
            # 3. 并且函数存在于index.py而非别的文件导入进去的
            # 4. 并且函数有文档字符串
            if (
                    inspect.isfunction(obj) and
                    not name.startswith('_') and
                    obj.__module__ == f'plugins.{folder}.index' and
                    inspect.getdoc(obj) is not None
            ):
                # 创建并启动线程来执行插件函数
                plugin_thread = threading.Thread(target=execute_plugin, args=(session, obj))
                plugin_thread.start()

    # __开头的文件都不会被加载
    for folder in [d for d in os.listdir('./plugins') if os.path.isdir(os.path.join('./plugins', d)) and not d.startswith('__')]:
        load_and_execute_plugins(session, folder)





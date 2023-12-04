
import importlib
import inspect
import os

from session_filter import ban_manager
from session_maker import event_to_session


data_nil = {
    'self_id': '',
    'platform': '',
    'timestamp': 0,  # 时间戳通常是一个数字，所以这里设置为0
    'type': '',
    'subtype': '',
    'message': {
        'id': '',
        'elements': [],  # 空列表
        'content': '1 1'
    },
    'user': {
        'id': '',
        'name': '',
        'avatar': ''
    },
    'member': {
        'user': {
            'id': '',
            'name': '',
            'avatar': ''
        },
        'nick': ''
    },
    'guild': {
        'id': '',
        'name': '',
        'avatar': ''
    },
    'channel': {
        'id': '',
        'type': 0,  # 假设这是一个数字类型
        'name': ''
    },
    'id': 0  # 假设这是一个数字类型
}


class PluginLoader:
    def __init__(self):
        self.loaded_plugins = {}

    def load_plugins(self):
        session = event_to_session(data_nil)
        for folder in [d for d in os.listdir('./plugins') if os.path.isdir(os.path.join('./plugins', d)) and not d.startswith('__')]:
            # print(f'[load_plugins] 正在加载插件包 [{folder}]')
            module = importlib.import_module(f'plugins.{folder}.index')
            for name, obj in inspect.getmembers(module):
                #         # 1. 如果是函数
                if not (
                        inspect.isfunction(obj) and
                        # not name.startswith('_') and
                        obj.__module__ == f'plugins.{folder}.index'
                        # and inspect.getdoc(obj) is not None
                ):
                    continue
                # 这个语句是为了在「不是插件的函数」传递「session」时抛出异常时结束这本次导入
                try:
                    obj(session)
                except:
                    continue
                if not hasattr(obj, 'enable_feature'):
                    continue
                self.loaded_plugins[name] = obj
                print(f'[load_plugins] [{folder}] 加载插件 [{obj.__name__}]')

    def execute_plugin(self, session, plugin_name):
        if plugin_name in self.loaded_plugins:
            obj = self.loaded_plugins[plugin_name]
            if ban_manager.check_before_plugin(session, obj.__name__):
                obj(session)

    def get_loaded_plugins_list(self):
        return self.loaded_plugins


plugin_loader = PluginLoader()







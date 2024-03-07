import inspect
import yaml
import registers
from typing import List, Callable


config: dict = yaml.safe_load(open('./config.yml', encoding='utf-8'))


class RegManager:
    def __init__(self):
        self.loaded_func = []
        self.satori_post = []
        self.before_request = []
        self.before_event = []
        self.before_plugin_do = []
        self.after_request = []
        self.after_event = []

        self.is_loaded = False

    def format_msg(self, on_list: List[Callable] = None):
        msg = ''
        if not on_list:
            msg += '| None |'
            return msg
        # 找出最长的函数名长度
        max_length = max(len(func.__name__) for func in on_list)
        # 打印每个函数名，同时在行尾添加 '|' 并保持对齐
        for i, func in enumerate(on_list):
            msg += '\033[32m●\033[0m '
            msg += f'[{i+1}]' + '   ' if i < 9 else f'[{i+1}]' + '  ' if i < 99 else f'[{i+1}]' + ' '
            msg += ('{:<{}}   '.format(func.__name__, max_length))
            msg += '.\n'
        # 打印表尾===
        # 清空列表
        del on_list
        return msg

    def load_plugin_from_register(self):
        module_list = inspect.getmembers(registers)
        # print(module_list)

        for _, obj in module_list:

            if not inspect.isfunction(obj):
                continue
            if not inspect.signature(obj).parameters:
                continue
            # print(f'[load_modules] {obj.__module__}.{obj.__name__} loaded.')
            # 根据属性将函数添加到对应的列表中，并默认设置为启用（True）
            if hasattr(obj, 'enable_feature'):
                self.loaded_func.append(obj)
            # if hasattr(obj, 'is_satori_post'):
            #     self.satori_post.append(obj)
            if hasattr(obj, 'is_before_request'):
                self.before_request.append(obj)
            if hasattr(obj, 'is_before_event'):
                self.before_event.append(obj)
            if hasattr(obj, 'is_before_plugin_do'):
                self.before_plugin_do.append(obj)
            if hasattr(obj, 'is_after_request'):
                self.after_request.append(obj)
            if hasattr(obj, 'is_after_event'):
                self.after_event.append(obj)

    def load_plugins(self):

        self.load_plugin_from_register()

        print('registers loaded.')

        all_on = registers_manager.loaded_func + registers_manager.satori_post + registers_manager.before_request + registers_manager.before_event + registers_manager.before_plugin_do + registers_manager.after_request + registers_manager.after_event
        formatted_msg = self.format_msg(all_on)
        print(formatted_msg)

        self.is_loaded = True


registers_manager = RegManager()





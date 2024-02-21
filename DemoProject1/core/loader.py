import importlib
import inspect
import os
import yaml


config: dict = yaml.safe_load(open('./config.yml', encoding='utf-8'))


class PluginManager:
    def __init__(self):
        self.loaded_func = []
        self.satori_post = []
        self.before_request = []
        self.before_event = []
        self.before_plugin_do = []
        self.after_request = []
        self.after_event = []

        self.is_loaded = False

    def load_plugin_from_folder(self, plugin_folder):
        module_path = f'{plugin_folder}'
        module = importlib.import_module(module_path)
        # print(module.__file__)

        # add __feature__ to module
        # setattr(module, '__feature__', 'modules/__feature__')
        module_list = inspect.getmembers(module)
        # print(module_list)

        for _, obj in module_list:

            if not inspect.isfunction(obj):  #  and obj.__module__ == module_path
                # try:
                #     print(f'[load_modules] {obj.__module__}.{obj.__name__} is not a function, skipped.')
                # except AttributeError:
                #     print(f'[load_modules] {obj} is not a function, skipped.')
                continue
            if not inspect.signature(obj).parameters:
                # try:
                #     print(f'[load_modules] {obj.__module__}.{obj.__name__} has no parameters, skipped.')
                # except AttributeError:
                #     print(f'[load_modules] {obj} has no parameters, skipped.')
                continue
            # print(f'[load_modules] {obj.__module__}.{obj.__name__} loaded.')
            # 根据属性将函数添加到对应的列表中，并默认设置为启用（True）
            if hasattr(obj, 'enable_feature'):
                self.loaded_func.append(obj)
            if hasattr(obj, 'is_satori_post'):
                self.satori_post.append(obj)
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

        self.load_plugin_from_folder('register')

        print('[load_modules] finished.')
        self.is_loaded = True


plugin_manager = PluginManager()





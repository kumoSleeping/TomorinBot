import inspect
import yaml
# import registers
from typing import List, Callable
from core.log import log
import pkgutil
import importlib.util
import os
import sys



config: dict = yaml.safe_load(open('./config.yml', encoding='utf-8'))


class RegManager:
    def __init__(self):
        self.loaded_func = []
        self.before_request = []
        self.before_event = []
        self.before_plugin_do = []
        self.after_request = []
        self.after_event = []
        
        self.is_loaded = False

    def load_plugin_from_register(self):
        plug_dir = './plugs'
        ban_list = config['core'].get('off_plugs', [])
        if ban_list:
            log.warning('Plugs disabled: {}'.format(ban_list))
        else:
            ban_list = []
        plug_list = [name for _, name, _ in pkgutil.iter_modules([plug_dir]) if name not in ban_list]
        # print(plug_list)
        sys.path.append(plug_dir)

        module_list = []
        for plug in plug_list:
            spec = importlib.util.spec_from_file_location(plug, os.path.join(plug_dir, plug, '__init__.py'))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module_list.append((plug, module))
        
        # print(module_list)

        # 遍历所有模块，找到函数并根据其属性进行分类
        for _, module in module_list:
            # 获取模块中所有的函数
            for name, obj in inspect.getmembers(module, inspect.isfunction):
                # 使用字典映射属性到对应的列表
                attr_to_list = {
                    'enable_feature': self.loaded_func,
                    'is_before_request': self.before_request,
                    'is_before_event': self.before_event,
                    'is_before_plugin_do': self.before_plugin_do,
                    'is_after_request': self.after_request,
                    'is_after_event': self.after_event,
                }
                # 检查每个属性并在必要时将函数添加到对应的列表中
                for attr, list_ref in attr_to_list.items():
                    if hasattr(obj, attr):
                        list_ref.append(obj)
                        break  # 假设一个函数只符合一个分类，找到即停止
      
    def print_msg(self, on_list=None):
        if not on_list:
            log.error('No functions loaded.')
            return
        max_name_length = max(len(func.__name__) for func in on_list)
        for i, func in enumerate(on_list):
            # 格式化序号前的空格
            num_space = '   ' if i < 9 else '  ' if i < 99 else ' '
            # 计算每个函数名后需要填充的空格数，以确保点（.）对齐
            padding = max_name_length - len(func.__name__)
            log.success('[{}]{}{}   {}.'.format(i+1, num_space, func.__name__, ' ' * padding))

    
    def load_plugins(self):
        self.load_plugin_from_register()
        log.info('registers loaded.')
        all_on = registers_manager.loaded_func + registers_manager.before_request + registers_manager.before_event + registers_manager.before_plugin_do + registers_manager.after_request + registers_manager.after_event
        self.print_msg(all_on)

        self.is_loaded = True


registers_manager = RegManager()





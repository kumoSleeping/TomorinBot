import inspect
from core.log import log
from core.external import config


class RegManager:
    def __init__(self):
        self.standard_event = []
        self.before_request = []
        self.before_event = []
        self.before_plugs = []
        self.after_request = []
        self.after_event = []

    def load_plugins(self):
        import plugs
        module_list = [(name, module) for name, module in inspect.getmembers(plugs, inspect.isfunction)]
        # 遍历所有模块，找到函数并根据其属性进行分类
        log.info(f'RUNNING >._ load registry...')
        log.info('IDX    FUNCTION NAME       ATTRIBUTE')
        idx = 0
        for name, module in module_list:
            # 使用字典映射属性到对应的列表
            attr_to_list = {
                'standard_event': self.standard_event,
                'before_request': self.before_request,
                'before_event': self.before_event,
                'before_plugs': self.before_plugs,
                'after_request': self.after_request,
                'after_event': self.after_event,
            }
            # 检查每个属性并在必要时将函数添加到对应的列表中
            for attr, list_ref in attr_to_list.items():
                if hasattr(module, attr):
                    num_space = '   ' if idx < 9 else '  ' if idx < 99 else ' '
                    idx += 1
                    padding = 18 - len(name)
                    log.success('{}.{}  {} {} [{}]'.format(idx, num_space, name, ' ' * padding, attr))
                    list_ref.append(module)
                    break  # 假设一个函数只符合一个分类，找到即停止
        log.success(f'RUNNING >._ load registry complete.')


registers_manager = RegManager()


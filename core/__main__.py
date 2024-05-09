import os
import sys
import inspect
import signal
from core.classes.utils import config_pre as config
from core.classes.utils import log


# 获取当前文件的父目录并切换工作目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
os.chdir(parent_directory)
sys.path.append(parent_directory)


class IManager:
    def __init__(self):
        self._satori_event = []
        self._startup = []
        self._api_requested = []
        self._event_built = []
        self.loaded = False

    def run_on_bot_started(self):
        if len(self._startup) > 0:
            log.info(f'> bot:started function started...')
            for func in self._startup:
                try:
                    func()
                    log.info(f"✓ bot:started function <{func.__name__}> executed.")
                except Exception as e:
                    log.error(f"✗ Error in bot_started function {func.__name__}: {e}")
            log.success(f'✓ bot:started function completed.')
        else:
            log.info(f'✓ bot:started function not found.')

    def load_plugins(self):
        import plugs
        module_list = [(name, module) for name, module in inspect.getmembers(plugs, inspect.isfunction)]
        # 遍历所有模块，找到函数并根据其属性进行分类
        log.info(f'> load registry...')
        log.info('IDX     FUNCTION NAME      ATTRIBUTES_TAG')
        log.info('---     -------------      --------------')
        idx = 0
        for name, module in module_list:
            # 使用字典映射属性到对应的列表
            attr_to_list = {
                '_satori_event': self._satori_event,
                '_startup': self._startup,  # 机器人启动时执行函数
                '_api_requested': self._api_requested,
                '_event_built': self._event_built
            }
            # 检查每个属性并在必要时将函数添加到对应的列表中
            for attr, list_ref in attr_to_list.items():
                # print(attr, list_ref)
                if hasattr(module, attr):
                    # 输出函数 attr 的值
                    # print(type(module))
                    # print(f"{attr} value: {getattr(module, attr)}")
                    num_space = '   ' if idx < 9 else '  ' if idx < 99 else ' '
                    idx += 1
                    padding = 18 - len(name)
                    log.success('({}){}  {} {}{}'.format(idx, num_space, name, ' ' * padding, getattr(module, attr)))
                    list_ref.append(module)
                    break  # 假设一个函数只符合一个分类，找到即停止
        log.success(f'✓ load registry complete.')
        self.loaded = True

    def initialize(self):
        self.load_plugins()  # 加载插件
        self.run_on_bot_started()  # 执行机器人启动时执行函数
        from core.transmit.bot_websockets import start_ws
        start_ws()  # 启动 websocket


initialize_manager = IManager()


if __name__ == '__main__':
    from core.__init__ import __version__
    print(f' ----------------------------------------------------------------- ')
    print(f'| TomorinBOT - v{__version__} - @2023-2024 Compliant with Satori Protocol |')
    print(f' ----------------------------------------------------------------- ')
    try:
        initialize_manager.initialize()
        while True:
            cmd = input()  # 阻塞主线程，保持程序运行
            if cmd in ['exit', 'kill', 'quit', 'stop']:
                log.warning(f'kill signal received.')
                os.kill(os.getpid(), signal.SIGTERM)
            log.warning(f'Command not found: {cmd}')
    except KeyboardInterrupt:
        log.info(f'かつて忘れられない、星空は未来を照らし、次の春へ。    ―― 2024.1.30 10:54:23・東京・豊島区')
        os.kill(os.getpid(), signal.SIGTERM)













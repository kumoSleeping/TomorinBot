import os
import sys
import inspect
import signal


# 获取当前文件的父目录并切换工作目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
os.chdir(parent_directory)
sys.path.append(parent_directory)


def start():
    from core.ws_transmit import start_ws
    start_ws()
    from core.config import registers_manager
    registers_manager.load_plugins()
    input()


def end(sig, frame):
    from core.log import log
    log.info(f'''かつて忘れられない、星空は未来を照らし、次の春へ。
――「2024.1.30 10:54:23・東京・豊島区」
''')
    sys.exit(0)


# 设置SIGINT信号处理函数
signal.signal(signal.SIGINT, end)


if __name__ == '__main__':
    from core.__init__ import __version__
    from core.loader import config
    config.need('log', {'color': True, 'debug': False})
    from core.log import log
    log.success(f'RUNNING >._ Tomorin BOT - v{__version__} @2023-2024')

    start()











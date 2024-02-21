import os
import sys
import inspect
import signal


# 获取当前文件的父目录并切换工作目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
os.chdir(parent_directory)
sys.path.append(parent_directory)


def start():
    # chick()
    from core.loader import plugin_manager
    plugin_manager.load_plugins()
    input()


def end(sig, frame):
    ascii_tmr = '''
かつて忘れられない、星空は未来を照らし、次の春へ。
――「2024.1.30 10:54:23・東京・豊島区」
'''
    print(f'\n{ascii_tmr}\n[core] off.')
    sys.exit(0)


# 设置SIGINT信号处理函数
signal.signal(signal.SIGINT, end)


if __name__ == '__main__':
    from core.__init__ import __version__
    ascii_tmr = f'''\033[34m
  ██████████╗   ███████╗    
   ╚══██╔████╗ ████╔══██╗   
      ██║██╔████╔██████╔╝   
      ██║██║╚██╔╝██╔══██╗   
      ██║██║ ╚═╝ ██║  █████║   
      ╚═╝╚═╝     ╚═╝  ╚════╝  v{__version__} @2023
\033[0m'''

    print(ascii_tmr)
    from core.loader import config

    if config['core']['hot_reload']:
        import hupper
        reloader = hupper.start_reloader('core.__main__.start',)

    else:
        start()












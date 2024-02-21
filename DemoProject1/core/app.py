import os
import sys
import inspect


# 获取当前文件的父目录并切换工作目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
os.chdir(parent_directory)
sys.path.append(parent_directory)


def st():
    # chick()
    from core.loader import plugin_manager
    plugin_manager.load_plugins()
    input()


if __name__ == '__main__':
    ascii_tmr = '''

      ██████████╗   ███████╗    
       ╚══██╔████╗ ████╔══██╗   
          ██║██╔████╔██████╔╝   
          ██║██║╚██╔╝██╔══██╗   
          ██║██║ ╚═╝ ██║  █████║   
          ╚═╝╚═╝     ╚═╝  ╚════╝  lite @2023

    '''

    ascii_tmr = '\033[34m' + ascii_tmr + '\033[37m' + '''
    かつて忘れられない、星空は未来を照らし、次の春へ。
    　　　　　　　　　　　　――「未来のある日・東京・豊島区」

     ''' + '\033[0m'

    print(ascii_tmr)
    from loader import config

    if config['core']['hot_reload']:
        import hupper
        reloader = hupper.start_reloader('core.app.st',)

    else:
        st()




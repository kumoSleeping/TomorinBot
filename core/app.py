import os
import sys
import inspect
import time


# 获取当前文件的父目录并切换工作目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
os.chdir(parent_directory)
sys.path.append(parent_directory)


def main():
    from core.loader import load_plugins
    import threading

    # 启动线程
    threading.Thread(target=load_plugins, daemon=True).start()
    os.environ['keep_alive'] = 'True'
    # 保持主线程运行
    while True:
        time.sleep(1.14)


if __name__ == '__main__':
    from loader import config
    if config['core']['hot_reload']:
        import hupper
        print('\033[31m[core] 已启用热重载\033[0m')
        reloader = hupper.start_reloader('core.app.main')
    else:
        main()







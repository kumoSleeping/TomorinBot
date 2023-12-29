import os
import sys
import inspect
import time

# 获取当前文件的父目录并切换工作目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
os.chdir(parent_directory)
sys.path.append(parent_directory)


if __name__ == '__main__':
    from core.loader import load_plugins
    import threading
    # 启动线程
    threading.Thread(target=load_plugins).start()
    # 保持主线程运行
    input()












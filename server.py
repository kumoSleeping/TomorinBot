import os
from pathlib import Path
import subprocess


# 获取当前脚本文件所在目录的绝对路径
script_directory = os.path.dirname(os.path.abspath(__file__))

# 构建 Ano.py 的路径
# print('正在挂起Ano.py')
print('当前 Tomorin 框架版本：[ 人間になりたいうた ]')

# 我们的迷失，从Ano酱开始
subprocess.run(["python", script_directory + '/core/AnonTokyo.py'])  # 同步websocket-client
# subprocess.run(["python", script_directory + '/core/Ano.py'])  # 异步websockets




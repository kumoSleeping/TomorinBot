import subprocess
import os


# 获取当前脚本文件所在目录的绝对路径
script_directory = os.path.dirname(os.path.abspath(__file__))


# 我们的迷失，从Anochan开始。
subprocess.run(["python", script_directory + '/core/anochan.py'])


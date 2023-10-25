import subprocess
import os


# 获取当前脚本文件所在目录的绝对路径
script_directory = os.path.dirname(os.path.abspath(__file__))

print('DEV模式启动，请再次运行 server.py \n所有组件日志将在此处显示。')
# 曾经不会被忘记，星空会照亮未来，下一个春天。
subprocess.run(["python", script_directory + '/core/sakiko.py'])  # 同步websocket-client



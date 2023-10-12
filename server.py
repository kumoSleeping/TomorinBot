import yaml
import os, inspect

# 获取当前代码所在文件的位置（包括文件名）
current_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
# 获取当前代码所在文件的目录
current_file_directory = os.path.dirname(current_file_path)

# 读取YAML文件
with open(current_file_directory + '/config.yml', 'r') as file:
    config = yaml.safe_load(file)

IP = config['server']["ip"]
PORT = config['server']["port"]
TOKEN = config['server']["token"]
Heartbeat_cd: int = config['server']["HeartbeatInterval"]
administrator: list = config['user']["administrator"]

import core

print('Tomorin-core 导入成功\nBGM: 人間になりたいうた')

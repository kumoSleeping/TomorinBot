import yaml

# 读取YAML文件
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

IP = config['server']["ip"]
PORT = config['server']["port"]
TOKEN = config['server']["token"]
Heartbeat_cd = config['server']["HeartbeatInterval"]

import core

print('人間になりたいうた...')

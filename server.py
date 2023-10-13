import os,\
    inspect,\
    yaml

# os.path.abspath(inspect.getfile(inspect.currentframe())) 获取当前代码所在文件的位置（包括文件名）
# os.path.dirname()获取当前代码所在文件的目录
# 读取YAML文件
config = yaml.safe_load(open(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                             + '/config.yml', 'r'))

IP, PORT, TOKEN, Heartbeat_cd, ADMINISTRATOR_list = config['server']["ip"], config['server']["port"],\
    config['server']["token"], config['server']["HeartbeatInterval"], config['user']["administrator"]

import core

print('Tomorin-core 导入成功\nBGM: 人間になりたいうた')



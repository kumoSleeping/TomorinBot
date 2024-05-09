import os
import inspect
from mods import config


config.need('auth', [
        {
          "platform": "red",
          "admin": [
            "114514"
          ]
        },
        {
          "platform": "chronocat",
          "admin": [
            "114514"
          ]
        }
      ])


def assets(file_name: str) -> str:
    '''
    自动分配 assets 文件路径
    '''
    file_path = inspect.stack()
    # 定位 plugs 文件夹
    for i in range(len(file_path)):
        if 'plugs' in file_path[i].filename:
            break
    if i == len(file_path):
        raise Exception('未找到 plugs 文件夹')
    else:
        # 定位 plugs 文件夹下的文件夹
        folder_name = os.path.dirname(file_path[i].filename)
        mixed_folder_name = f"{folder_name}/{file_name}"
        return mixed_folder_name


def is_admin(platform, user_id):
    '''
    实现根据配置文件，判断是否 admin
    '''
    for auth in config.get_key('auth'):
        if auth['platform'] == platform:
            if str(user_id) in auth['admin']:
                return True
    return False








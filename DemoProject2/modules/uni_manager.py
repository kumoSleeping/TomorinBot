from core import config
import os
import inspect

if config['asset_path']['assets-dir'] and not os.path.exists(config['asset_path']['assets-dir']):
    os.mkdir(config['asset_path']['assets-dir'])

ASSETS_DIR = config['asset_path']['assets-dir']

if 'auth' not in config:
    config['auth'] = []


def auto_asset_path():
    '''
    实现根据配置文件，自动获取该模块的所分配的资源文件夹路径


    Automatically get the resource folder path assigned to the module according to the configuration file
    '''
    file_path = inspect.stack()[1].filename
    folder_name = os.path.dirname(file_path)
    pure_folder_name = os.path.basename(folder_name)
    mixed_folder_name = f"{ASSETS_DIR}/{pure_folder_name}"
    # 创建pure_folder_name
    if not os.path.exists(mixed_folder_name):
        os.mkdir(mixed_folder_name)
    return mixed_folder_name


def is_admin(platform, user_id):
    '''
    实现根据配置文件，平台，用户id判断是否是管理员


    Realize whether it is an administrator according to the configuration file, platform, and user id
    '''
    for auth in config['auth']:
        if auth['platform'] == platform:
            if str(user_id) in auth['admin']:
                return True
    return False








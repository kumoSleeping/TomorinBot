import os
import inspect
import json
from core.log import log


class Config:
    def __init__(self, config_file_path):
        self.data = {}
        self.config_file_path = config_file_path
        self._load_config()

    def _load_config(self):
        try:
            with open(self.config_file_path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"Config file {self.config_file_path} not found.")
            # self.data = {}
            # self._save_config()

    def _save_config(self):
        with open(self.config_file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def need(self, key, default_value=None):
        if key not in self.data:
            # log.warning(f"Key '{key}' not found in config. Adding it with default value.")
            self.data[key] = default_value
            self._save_config()
            log.error(f"Config '{key}' updated. Please close the program and edit the config file.")
            # exit()

    def get_key(self, key):
        return self.data.get(key)
    
    
config = Config('config.json')


config.need('asset_path', 'assets')
assets_path = config.get_key('asset_path')

if not os.path.exists(assets_path):
    os.mkdir(assets_path)

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


def auto_asset_path():
    '''
    实现根据配置文件，自动获取该模块的所分配的资源文件夹路径


    Automatically get the resource folder path assigned to the module according to the configuration file
    '''
    file_path = inspect.stack()[1].filename
    folder_name = os.path.dirname(file_path)
    pure_folder_name = os.path.basename(folder_name)
    mixed_folder_name = f"{assets_path}/{pure_folder_name}"
    # 创建pure_folder_name
    if not os.path.exists(mixed_folder_name):
        os.mkdir(mixed_folder_name)
    return mixed_folder_name


def is_admin(platform, user_id):
    '''
    实现根据配置文件，平台，用户id判断是否是管理员


    Realize whether it is an administrator according to the configuration file, platform, and user id
    '''
    for auth in config.get_key('auth'):
        if auth['platform'] == platform:
            if str(user_id) in auth['admin']:
                return True
    return False








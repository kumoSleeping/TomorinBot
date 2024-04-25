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
    告诉你文件在哪里
    '''
    file_path = inspect.stack()[1].filename
    folder_name = os.path.dirname(file_path)
    # pure_folder_name = os.path.basename(folder_name)
    mixed_folder_name = f"{folder_name}/{file_name}"
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








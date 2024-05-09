import time
import json
import os
import inspect
from datetime import datetime
import sys


ansi_color = True


class Log:
    @staticmethod
    def debug(text):
        """
        实现自定义print函数 (只有在配置文件启用的时候才会被显示的展示出来)
        Implement custom print function (only displayed when the configuration file is enabled)
        """
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        filename_parts = inspect.stack()[1].filename.split(os.path.sep)[-3:-1]
        text = log_time + ' [' + '-'.join(filename_parts) + '] ' + str(text)
        # if config["log"]["debug"]:
        if ansi_color:
            print("\033[1;31m■ " + text + "\033[0m")
        else:
            print("DEBUG__ - " + text)

    @staticmethod
    def error(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        filename_parts = inspect.stack()[1].filename.split(os.path.sep)[-3:-1]
        text = log_time + ' [' + '-'.join(filename_parts) + '] ' + str(text)
        if ansi_color:
            print("\033[1;31m● " + text + "\033[0m")
        else:
            print("ERROR__ - " + text)

    @staticmethod
    def info(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        filename_parts = inspect.stack()[1].filename.split(os.path.sep)[-3:-1]
        text = log_time + ' [' + '-'.join(filename_parts) + '] ' + str(text)
        if ansi_color:
            print("\033[1;37m● " + "\033[0m" + text)
        else:
            print("INFO___ - " + text)

    @staticmethod
    def warning(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        filename_parts = inspect.stack()[1].filename.split(os.path.sep)[-3:-1]
        text = log_time + ' [' + '-'.join(filename_parts) + '] ' + str(text)
        if ansi_color:
            print("\033[1;33m● " + text + "\033[0m")
        else:
            print("WARNING - " + text)

    @staticmethod
    def success(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        filename_parts = inspect.stack()[1].filename.split(os.path.sep)[-3:-1]
        text = log_time + ' [' + '-'.join(filename_parts) + '] ' + str(text)
        if ansi_color:
            print("\033[1;32m● " + "\033[0m" + text)
        else:
            print("SUCCESS - " + text)


# log 包是第一个被加载的包，所以在这里初始化配置文件
if not os.path.exists("config.json"):
    # 写入空配置文件
    with open("config.json", "w", encoding="utf-8") as f:
        f.write(json.dumps({}, indent=4))
    log = Log()
    log.warning("Config file not found, created a new one.")
else:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.loads(f.read())
    log = Log()


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
    def _save_config(self):
        with open(self.config_file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def need(self, key, default_value=None):
        if key not in self.data:
            self.data[key] = default_value
            self._save_config()
            log.error(f"Config '{key}' updated. Please close the program and edit the config file.")

    def get_key(self, key):
        return self.data.get(key)


config_pre = Config('config.json')







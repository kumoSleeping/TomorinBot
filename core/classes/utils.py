import time
import json
import os
import inspect
from datetime import datetime


class C:
    reset = "\033[0m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"
    white = "\033[37m"
    # Bright variants
    bright_red = "\033[91m"
    bright_green = "\033[92m"
    bright_yellow = "\033[93m"
    bright_blue = "\033[94m"
    bright_magenta = "\033[95m"
    bright_cyan = "\033[96m"
    bright_white = "\033[97m"

    class bg:  # Background colors
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        yellow = "\033[43m"
        blue = "\033[44m"
        magenta = "\033[45m"
        cyan = "\033[46m"
        white = "\033[47m"
        # Bright variants
        bright_black = "\033[100m"
        bright_red = "\033[101m"
        bright_green = "\033[102m"
        bright_yellow = "\033[103m"
        bright_blue = "\033[104m"
        bright_magenta = "\033[105m"
        bright_cyan = "\033[106m"
        bright_white = "\033[107m"

    class style:
        bold = "\033[1m"
        underline = "\033[4m"
        reversed = "\033[7m"
        dim = "\033[2m"
        italic = "\033[3m"
        blink = "\033[5m"


c = C()


class Log:
    @staticmethod
    def debug(text):
        """
        实现自定义print函数 (只有在配置文件启用的时候才会被显示的展示出来)
        Implement custom print function (only displayed when the configuration file is enabled)
        """
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        filename_parts = inspect.stack()[1].filename.split(os.path.sep)[-3:-1]
        if filename_parts[-1] in ['core', 'mods', 'plugs']:
            selected_parts = filename_parts[-1]
        else:
            selected_parts = '-'.join(filename_parts)
        print(f'{c.bright_magenta}▶{c.white} {log_time} {c.cyan}{selected_parts} {c.bright_magenta}{text}{c.reset}')

    @staticmethod
    def error(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        filename_parts = inspect.stack()[1].filename.split(os.path.sep)[-3:-1]
        if filename_parts[-1] in ['core', 'mods', 'plugs']:
            selected_parts = filename_parts[-1]
        else:
            selected_parts = '-'.join(filename_parts)
        print(f'{c.bright_red}✗{c.white} {log_time} {c.cyan}{selected_parts} {c.bg.red}{c.bright_white}{text}{c.reset}')

    @staticmethod
    def info(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        filename_parts = inspect.stack()[1].filename.split(os.path.sep)[-3:-1]
        if filename_parts[-1] in ['core', 'mods', 'plugs']:
            selected_parts = filename_parts[-1]
        else:
            selected_parts = '-'.join(filename_parts)
        print(f'●{c.white} {log_time} {c.cyan}{selected_parts}{c.reset} {text}')

    @staticmethod
    def warning(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        filename_parts = inspect.stack()[1].filename.split(os.path.sep)[-3:-1]
        if filename_parts[-1] in ['core', 'mods', 'plugs']:
            selected_parts = filename_parts[-1]
        else:
            selected_parts = '-'.join(filename_parts)
        print(f'{c.yellow}⚠{c.white} {log_time} {c.cyan}{selected_parts}{c.bright_yellow} {c.bg.yellow}{c.bright_white}{text}{c.reset}')

    @staticmethod
    def success(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        filename_parts = inspect.stack()[1].filename.split(os.path.sep)[-3:-1]
        if filename_parts[-1] in ['core', 'mods', 'plugs']:
            selected_parts = filename_parts[-1]
        else:
            selected_parts = '-'.join(filename_parts)
        print(f'{c.bright_green}✓{c.white} {log_time} {c.cyan}{selected_parts} {c.reset}{text}')


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




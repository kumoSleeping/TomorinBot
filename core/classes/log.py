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
    def get_caller_name(caller):
        caller_path_list = caller.filename.split(os.path.sep)

        if 'core' in caller_path_list[-2]:
            pkgs = 'core'
        elif caller.filename.endswith('__init__.py'):
            pkgs = caller.filename.split(os.path.sep)[-2]
        else:
            pkgs = caller.filename.split(os.path.sep)[-1]

        if pkgs.endswith('.py'):
            pkgs = pkgs[:-3]

        return pkgs

    @staticmethod
    def debug(text):
        """
        实现自定义print函数 (只有在配置文件启用的时候才会被显示的展示出来)
        Implement custom print function (only displayed when the configuration file is enabled)
        """
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        caller_name = Log.get_caller_name(inspect.stack()[1])
        print(f'{c.bright_magenta}▶{c.white} {log_time} {c.cyan}{caller_name} {c.bright_magenta}{text}{c.reset}')

    @staticmethod
    def error(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        caller_name = Log.get_caller_name(inspect.stack()[1])
        print(f'{c.bright_red}✗{c.white} {log_time} {c.cyan}{caller_name} {c.bg.red}{c.bright_white}{text}{c.reset}')

    @staticmethod
    def info(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        caller_name = Log.get_caller_name(inspect.stack()[1])
        print(f'●{c.white} {log_time} {c.cyan}{caller_name}{c.reset} {text}')

    @staticmethod
    def warning(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        caller_name = Log.get_caller_name(inspect.stack()[1])
        print(f'{c.yellow}⚠{c.white} {log_time} {c.cyan}{caller_name}{c.bright_yellow} {c.bg.yellow}{c.bright_white}{text}{c.reset}')

    @staticmethod
    def success(text):
        log_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        caller_name = Log.get_caller_name(inspect.stack()[1])
        print(f'{c.bright_green}✓{c.white} {log_time} {c.cyan}{caller_name} {c.reset}{text}')


log = Log()


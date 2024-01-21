import sys
import os
import datetime
from plugins.asset_path import auto_asset_path
from core.loader import config
import traceback
import inspect

path_ = auto_asset_path()


# 获取日志文件的路径
def get_log_file_path():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")  # 当前日期
    log_file = os.path.join(path_, f'log-{date_str}.txt')
    return log_file


# 自定义print函数
def log_print(*args, **kwargs):
    log_file_path = get_log_file_path()
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d ｜ %H:%M:%S")
    with open(log_file_path, 'a') as log_file:
        print(time_stamp, *args, **kwargs, file=log_file)  # 写入文件
        # print(time_stamp, *args, **kwargs)  # 同时打印到控制台


# 重定向标准错误输出
class StderrRedirector:
    def __init__(self):
        self.log_file = get_log_file_path()

    def write(self, message):
        with open(self.log_file, 'a') as log_file:
            time_ = datetime.datetime.now().strftime("%Y-%m-%d ｜ %H:%M:%S")
            if message == "Traceback (most recent call last):\n":
                log_file.write(f"{time_} ========================[ERROR]=======================\n{message}")
            # if 'time.sleep(1.14)' in message:
            # #     删除前两行
            #     message = message.split('\n')[5:]
            #     message = '\n'.join(message)
            #     log_file.write(f"{time_} ========================[END]=======================\n{message}")
            else:
                log_file.write(f"{message}")
        sys.__stderr__.write(message)

    def flush(self):
        pass


sys.stderr = StderrRedirector()
if not os.path.exists(path_):
    os.mkdir(path_)


def log(text: str):
    '''
    如果是开发模式，打印日志，如果不是，不打印
    '''
    if log_config := config['logger']['debug_package']:
        try:
            # 使用 os.path.sep 获取操作系统相关的路径分隔符
            caller = inspect.stack()[1].filename.split(os.path.sep)[-2]
        except IndexError:
            # 适当处理错误，例如记录错误信息或者使用默认值
            print('\033[1;33m[log] caller filename folder IndexError\033[0m')
            caller = "Unknown"

        # 检查是否应该记录这个调用者的日志
        if caller in log_config:
            print('\033[1;33m[log] ' + text + '\033[0m')





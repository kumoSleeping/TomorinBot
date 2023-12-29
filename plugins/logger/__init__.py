import sys
import os
import datetime


# 获取日志文件的路径
def get_log_file_path():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")  # 当前日期
    log_file = os.path.join('plugins/logger/output', f'log-{date_str}.txt')
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
            if 'time.sleep(1.14)' in message:
            #     删除前两行
                message = message.split('\n')[5:]
                message = '\n'.join(message)
                log_file.write(f"{time_} ========================[END]=======================\n{message}")
            else:
                log_file.write(f"{message}")
        sys.__stderr__.write(message)

    def flush(self):
        pass


sys.stderr = StderrRedirector()
if not os.path.exists('plugins/logger/output'):
    os.mkdir('plugins/logger/output')


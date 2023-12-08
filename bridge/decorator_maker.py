from functools import wraps
from datetime import datetime
import time
from threading import Thread
import schedule

from bridge.session_adder import Command
from core.event_decorator import OnEvent
on_event = OnEvent()


class OnActivator:
    @staticmethod
    def command(cmd: (str, list) = None):
        '''
        当命令被触发时触发。以 create-message 为底层事件。
        支持传入字符串列表作为多个触发词。
        如果没有提供 cmd 参数，则使用装饰的函数名作为命令，且此时不会被help命令识别。
        '''
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                wrapper.enable_feature = True
                # print(cmd)
                try:
                    session = args[0]

                except IndexError:
                    print('你 session 呢 IndexError')
                    return False
                pure_message = session.message.content

                if session.type != 'message-created':
                    return False

                # 判断是否传入了命令名
                command_names = cmd if isinstance(cmd, (list, tuple)) else [cmd]
                # 如果cmd是函数，或者没有提供cmd，则使用函数名
                if callable(cmd) or cmd is None:
                    command_names = [func.__name__]

                # 检查是否匹配任一命令名
                for command_name in command_names:
                    if pure_message.startswith(command_name + ' '):
                        cmd_list = pure_message.split()
                        command_args = cmd_list[1:]
                        text = pure_message.replace(command_name, '', 1)
                        if text.startswith(' '):
                            text = text.replace(' ', '', 1)
                        session.command = Command(command_name, command_args, text)
                        return func(session)
                    elif pure_message == command_name:
                        session.command = Command(command_name, None, '')
                        return func(session)
                return False

            return wrapper

        # 如果传入的 cmd 是函数，表示没有提供命令名，直接返回装饰器
        if callable(cmd):
            return decorator(cmd)
        else:
            return decorator  # 否则，返回装饰器函数

    @staticmethod
    def timer(time_or_times: (str, list)):
        """
        装饰器：在指定的24小时制时间（字符串或字符串列表）循环执行函数
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_run_time = None  # 跟踪上次执行时间
                is_executing = False  # 标志位，表示函数是否正在执行
                def scheduled_task():
                    nonlocal last_run_time, is_executing
                    # 如果函数正在执行，则跳过
                    if is_executing:
                        print('pass: is executing')
                        return
                    current_time = datetime.now()
                    # 检查上次执行时间是否与当前时间相同（分钟级别）
                    if last_run_time and current_time.minute == last_run_time.minute and current_time.hour == last_run_time.hour:
                        print('pass: time is same')
                        return
                    last_run_time = current_time  # 更新上次执行时间
                    is_executing = True
                    try:
                        print(f"[scheduler] Do [{func.__name__}] now!")
                        func()
                    finally:
                        time.sleep(1)  # 等待1秒，确保下一次执行不会在同一分钟内
                        is_executing = False  # 确保在函数执行结束后重置标志位
                # 判断传入的是单个时间字符串还是时间字符串列表
                times = [time_or_times] if isinstance(time_or_times, str) else time_or_times
                for time_str in times:
                    schedule.every().day.at(time_str).do(scheduled_task)
                # 启动一个线程来运行定时任务检查
                def run_schedule():
                    while True:
                        schedule.run_pending()
                        time.sleep(10)  # 每10秒检查一次
                        # print('op')

                schedule_thread = Thread(target=run_schedule)
                schedule_thread.start()
                print(f"[scheduler] [{func.__name__}] is scheduled for {times}.")
                return func
            return wrapper
        return decorator

    @staticmethod
    def interval(interval: int):
        """
        装饰器：在函数调用之间加入固定的时间间隔
        :param interval: 间隔时间（秒）
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                def interval_task():
                    # 执行日志
                    print(f"[interval] Do [{func.__name__}] now!")
                    func()

                # 启动一个线程来运行定时任务检查
                def run_interval():
                    time.sleep(3)  # 等待框架启动完成
                    while True:
                        interval_task()
                        time.sleep(interval)

                interval_thread = Thread(target=run_interval)
                interval_thread.start()

                print(f"[interval] Then [{func.__name__}] is scheduled for every {interval} seconds.")
                return func

            return wrapper

        return decorator


on_activator = OnActivator()




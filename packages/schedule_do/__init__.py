import time
from datetime import datetime
from functools import wraps
from threading import Thread
import schedule


def timer_do(time_or_times: str | list):
    """
    实现装饰器：定时执行器，以本地时间为基准，到达了预定的时间 (24小时制) 就执行一次任务

    参数:
    time_or_times: 一个时间字符串或者时间字符串列表，例如 '10:30' 或 ['10:30', '14:30']


    Implement decorator: a timed executor, based on local time, when the scheduled time (24-hour system) is reached, the task is executed once

    parameters:
    time_or_times: a time string or a list of time strings, such as '10:30' or ['10:30', '14:30']
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


def interval_do(interval: int, do_now: bool = True):
    """
    实现装饰器：实现循环计时器，每隔一段时间就执行一次任务，也就是在函数调用之间加入固定的时间间隔

    参数:
    interval: 间隔时间 (秒)
    do_now 是否在启动时立即执行一次 (默认为 True)


    Implement decorator: implement a loop timer, execute the task every once in a while, that is, add a fixed time interval between function calls

    parameters:
    interval: interval time (seconds)
    do_now: whether to execute once immediately at startup (default is True)
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
                time.sleep(0.5)  # 等待框架启动完成
                if not do_now:
                    time.sleep(interval)
                while True:
                    interval_task()
                    time.sleep(interval)

            interval_thread = Thread(target=run_interval)
            interval_thread.start()

            print(f"[interval] Then [{func.__name__}] is scheduled for every {interval} seconds.")
            return func

        return wrapper

    return decorator






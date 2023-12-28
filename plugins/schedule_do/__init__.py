import time
from datetime import datetime
from functools import wraps
from threading import Thread
import schedule


def timer_do(time_or_times: str | list):
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


def interval_do(interval: int, do_now: bool = True):
    """
    装饰器：在函数调用之间加入固定的时间间隔

    :param do_now: 是否在启动时立即执行一次
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






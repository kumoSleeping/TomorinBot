from functools import wraps
from datetime import datetime
import time
from threading import Thread
import schedule

from session_maker import Command
# from load_plugins import function_info_list


# def resister_function_info(function_name, function_docstring):
#     # print(f'[load_plugins] [{folder}] 扫描到函数 [{obj.__name__}]')
#     function_info = {
#         'function_name': function_name,
#         'function_docstring': function_docstring
#     }
#     function_info_list.append(function_info)


class OnEvent:
    @staticmethod
    def message_created(func):
        '''
        当消息被创建时触发。必需资源：channel，message，user。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'message-created':
                return func(session)

        return inner_wrapper

    @staticmethod
    def message_updated(func):
        '''
        当消息被编辑时触发。必需资源：channel，message，user。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'message-updated':
                return func(session)

        return inner_wrapper

    @staticmethod
    def message_deleted(func):
        '''
        当消息被删除时触发。必需资源：channel，message，user。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'message-deleted':
                return func(session)

        return inner_wrapper

    @staticmethod
    def interaction_button(func):
        '''
        当按钮被点击时触发。必需资源：button。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'interaction/button':
                return func(session)

        return inner_wrapper

    @staticmethod
    def interaction_command(func):
        '''
        调用斜线指令时触发。资源 argv 或 message 中至少包含其一。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'interaction/command':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_added(func):
        '''
        加入群组时触发。必需资源：guild。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-added':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_updated(func):
        '''
        群组被修改时触发。必需资源：guild。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-updated':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_removed(func):
        '''
        退出群组时触发。必需资源：guild。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-removed':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_request(func):
        '''
        接收到新的入群邀请时触发。必需资源：guild。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-request':
                return func(session)

        return inner_wrapper

    @staticmethod
    def login_added(func):
        '''
        登录被创建时触发。必需资源：login。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'login-added':
                return func(session)

        return inner_wrapper

    @staticmethod
    def login_removed(func):
        '''
        登录被删除时触发。必需资源：login。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'login-removed':
                return func(session)

        return inner_wrapper

    @staticmethod
    def login_updated(func):
        '''
        登录信息更新时触发。必需资源：login。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'login-updated':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_member_added(func):
        '''
        群组成员增加时触发。必需资源：guild，member，user。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-member-added':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_member_updated(func):
        '''
        群组成员信息更新时触发。必需资源：guild，member，user。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-member-updated':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_member_removed(func):
        '''
        群组成员移除时触发。必需资源：guild，member，user。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-member-removed':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_member_request(func):
        '''
        接收到新的加群请求时触发。必需资源：guild，member，user。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-member-request':
                return func(session)

        return inner_wrapper

    @staticmethod
    def friend_request(func):
        '''
        接收到新的好友申请时触发。必需资源：user。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'friend-request':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_role_created(func):
        '''
        群组角色被创建时触发。必需资源：guild，role。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-role-created':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_role_updated(func):
        '''
        群组角色被修改时触发。必需资源：guild，role。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-role-updated':
                return func(session)

        return inner_wrapper

    @staticmethod
    def guild_role_deleted(func):
        '''
        群组角色被删除时触发。必需资源：guild，role。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            session = args[0]
            inner_wrapper.enable_feature = True
            if session.type == 'guild-role-deleted':
                return func(session)

        return inner_wrapper


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
                        print('op')

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




from functools import wraps
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
                # inner_wrapper.enable_feature = True
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
    def command(cmd=None):
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


on_activator = OnActivator()




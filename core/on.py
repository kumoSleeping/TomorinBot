from functools import wraps


class On:
    @staticmethod
    def message_created(func):
        """
        当消息被创建时触发。必需资源：channel，message，user。
        """
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'message-created':
                return func(event)

        return inner_wrapper

    @staticmethod
    def message_updated(func):
        '''
        当消息被编辑时触发。必需资源：channel，message，user。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'message-updated':
                return func(event)

        return inner_wrapper

    @staticmethod
    def message_deleted(func):
        '''
        当消息被删除时触发。必需资源：channel，message，user。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'message-deleted':
                return func(event)

        return inner_wrapper

    @staticmethod
    def interaction_button(func):
        '''
        当按钮被点击时触发。必需资源：button。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'interaction/button':
                return func(event)

        return inner_wrapper

    @staticmethod
    def interaction_command(func):
        '''
        调用斜线指令时触发。资源 argv 或 message 中至少包含其一。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'interaction/command':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_added(func):
        '''
        加入群组时触发。必需资源：guild。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-added':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_updated(func):
        '''
        群组被修改时触发。必需资源：guild。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-updated':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_removed(func):
        '''
        退出群组时触发。必需资源：guild。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-removed':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_request(func):
        '''
        接收到新的入群邀请时触发。必需资源：guild。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-request':
                return func(event)

        return inner_wrapper

    @staticmethod
    def login_added(func):
        '''
        登录被创建时触发。必需资源：login。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'login-added':
                return func(event)

        return inner_wrapper

    @staticmethod
    def login_removed(func):
        '''
        登录被删除时触发。必需资源：login。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'login-removed':
                return func(event)

        return inner_wrapper

    @staticmethod
    def login_updated(func):
        '''
        登录信息更新时触发。必需资源：login。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'login-updated':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_member_added(func):
        '''
        群组成员增加时触发。必需资源：guild，member，user。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-member-added':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_member_updated(func):
        '''
        群组成员信息更新时触发。必需资源：guild，member，user。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-member-updated':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_member_removed(func):
        '''
        群组成员移除时触发。必需资源：guild，member，user。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-member-removed':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_member_request(func):
        '''
        接收到新的加群请求时触发。必需资源：guild，member，user。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-member-request':
                return func(event)

        return inner_wrapper

    @staticmethod
    def friend_request(func):
        '''
        接收到新的好友申请时触发。必需资源：user。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'friend-request':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_role_created(func):
        '''
        群组角色被创建时触发。必需资源：guild，role。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-role-created':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_role_updated(func):
        '''
        群组角色被修改时触发。必需资源：guild，role。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-role-updated':
                return func(event)

        return inner_wrapper

    @staticmethod
    def guild_role_deleted(func):
        '''
        群组角色被删除时触发。必需资源：guild，role。
        '''
        func.enable_feature = True

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            event = args[0]
            if event.type == 'guild-role-deleted':
                return func(event)

        return inner_wrapper

    # 内部接口
    @staticmethod
    def internal(target_event_type):

        def decorator(func):
            func.enable_feature = True

            @wraps(func)
            def inner_wrapper(*args, **kwargs):
                event = args[0]
                if event._type == target_event_type:
                    return func(*args, **kwargs)
            return inner_wrapper

        return decorator

    @staticmethod
    def before_request(func):
        """
        装饰器：在发送消息前执行函数

        被装饰函数的参数为 event:Event, method: str, data: dict, platform: str, self_id: str
        被装饰函数的返回值与参数相同
        """
        func.is_before_request = True
        return func

    @staticmethod
    def after_request(func):
        """
        装饰器：在发送消息后执行函数

        被装饰函数的参数为 event:Event, method: str, data: dict, platform: str, self_id: str, response_dict: dict
        被装饰函数的返回值与参数相同
        """
        func.is_after_request = True
        return func

    @staticmethod
    def before_event(func):
        """
        装饰器：在事件处理前执行函数

        被装饰函数的参数为 data: dict
        被装饰函数的返回值与参数相同
        """
        func.is_before_event = True
        return func

    @staticmethod
    def before_plugin_do(func):
        """
        装饰器：在插件执行前执行函数

        被装饰函数的参数为 event:Event, plugin_name: str
        被装饰函数的返回值与参数相同
        """
        func.is_before_plugin_do = True
        return func

    @staticmethod
    def after_event(func):
        """
        装饰器：在事件处理后执行函数

        被装饰函数的参数为 event:Event
        被装饰函数的返回值与参数相同
        """
        func.is_after_event = True
        return func


on = On()


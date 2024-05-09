from functools import wraps


class On:
    @staticmethod
    def message_created(func):
        """
        当消息被创建时触发。必需资源：channel，message，user。
        """
        func._satori_event = 'message-created'

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
        func._satori_event = 'message-updated'

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
        func._satori_event = 'message-deleted'

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
        func._satori_event = 'interaction/button'

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
        func._satori_event = 'interaction/command'

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
        func._satori_event = 'guild-added'

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
        func._satori_event = 'guild-updated'

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
        func._satori_event = 'guild-removed'

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
        func._satori_event = 'guild-request'

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
        func._satori_event = 'login-added'

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
        func._satori_event = 'login-removed'

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
        func._satori_event = 'login-updated'

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
        func._satori_event = 'guild-member-added'

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
        func._satori_event = 'guild-member-updated'

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
        func._satori_event = 'guild-member-removed'

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
        func._satori_event = 'guild-member-request'

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
        func._satori_event = 'friend-request'

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
        func._satori_event = 'guild-role-created'

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
        func._satori_event = 'guild-role-updated'

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
        func._satori_event = 'guild-role-deleted'

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
            func._satori_event = True

            @wraps(func)
            def inner_wrapper(*args, **kwargs):
                event = args[0]
                if event._type == target_event_type:
                    return func(*args, **kwargs)
            return inner_wrapper

        return decorator

    @staticmethod
    def bot_start_up(func):
        """
        装饰器：在机器人启动时执行函数
        """
        func._startup = 'bot:start-up'
        return func

    @staticmethod
    def bot_event_built(func):
        """
        装饰器：在机器人启动时执行函数
        """
        func._event_built = 'bot:event-built'
        return func

    @staticmethod
    def bot_api_requested(func):
        """
        装饰器：在机器人启动时执行函数
        """
        func._api_requested = 'bot:api-requested'
        return func


on = On()


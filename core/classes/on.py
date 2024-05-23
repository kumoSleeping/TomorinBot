

class On:
    @staticmethod
    def message_created(func):
        """
        Triggered when a message is created. Required resources: channel, message, user.
        当消息被创建时触发。必需资源：channel，message，user。
        """
        func._satori_event = 'message-created'
        return func

    @staticmethod
    def message_updated(func):
        """
        Triggered when a message is updated. Required resources: channel, message, user.
        当消息被编辑时触发。必需资源：channel，message，user。
        """
        func._satori_event = 'message-updated'
        return func

    @staticmethod
    def message_deleted(func):
        """
        Triggered when a message is deleted. Required resources: channel, message, user.
        当消息被删除时触发。必需资源：channel，message，user。
        """
        func._satori_event = 'message-deleted'
        return func

    @staticmethod
    def interaction_button(func):
        """
        Triggered when a button is clicked. Required resource: button.
        当按钮被点击时触发。必需资源：button。
        """
        func._satori_event = 'interaction/button'
        return func

    @staticmethod
    def interaction_command(func):
        """
        Triggered when a slash command is invoked. At least one of the resources argv or message must be included.
        调用斜线指令时触发。资源 argv 或 message 中至少包含其一。
        """
        func._satori_event = 'interaction/command'
        return func

    @staticmethod
    def guild_added(func):
        """
        Triggered when joining a guild. Required resource: guild.
        加入群组时触发。必需资源：guild。
        """
        func._satori_event = 'guild-added'
        return func

    @staticmethod
    def guild_updated(func):
        """
        Triggered when a guild is updated. Required resource: guild.
        群组被修改时触发。必需资源：guild。
        """
        func._satori_event = 'guild-updated'
        return func

    @staticmethod
    def guild_removed(func):
        """
        Triggered when exiting a guild. Required resource: guild.
        退出群组时触发。必需资源：guild。
        """
        func._satori_event = 'guild-removed'
        return func

    @staticmethod
    def guild_request(func):
        """
        Triggered when a new guild join request is received. Required resource: guild.
        接收到新的入群邀请时触发。必需资源：guild。
        """
        func._satori_event = 'guild-request'
        return func


    @staticmethod
    def login_added(func):
        """
        Triggered when a login is created. Required resource: login.
        登录被创建时触发。必需资源：login。
        """
        func._satori_event = 'login-added'
        return func

    @staticmethod
    def login_removed(func):
        """
        Triggered when a login is removed. Required resource: login.
        登录被删除时触发。必需资源：login。
        """
        func._satori_event = 'login-removed'
        return func

    @staticmethod
    def login_updated(func):
        """
        Triggered when login information is updated. Required resource: login.
        登录信息更新时触发。必需资源：login。
        """
        func._satori_event = 'login-updated'
        return func

    @staticmethod
    def guild_member_added(func):
        """
        Triggered when a guild member is added. Required resources: guild, member, user.
        群组成员增加时触发。必需资源：guild，member，user。
        """
        func._satori_event = 'guild-member-added'
        return func

    @staticmethod
    def guild_member_updated(func):
        """
        Triggered when guild member information is updated. Required resources: guild, member, user.
        群组成员信息更新时触发。必需资源：guild，member，user。
        """
        func._satori_event = 'guild-member-updated'
        return func

    @staticmethod
    def guild_member_removed(func):
        """
        Triggered when a guild member is removed. Required resources: guild, member, user.
        群组成员移除时触发。必需资源：guild，member，user。
        """
        func._satori_event = 'guild-member-removed'
        return func

    @staticmethod
    def guild_member_request(func):
        """
        Triggered when a new guild member request is received. Required resources: guild, member, user.
        接收到新的加群请求时触发。必需资源：guild，member，user。
        """
        func._satori_event = 'guild-member-request'
        return func

    @staticmethod
    def friend_request(func):
        """
        Triggered when a new friend request is received. Required resource: user.
        接收到新的好友申请时触发。必需资源：user。
        """
        func._satori_event = 'friend-request'
        return func

    @staticmethod
    def guild_role_created(func):
        """
        Triggered when a guild role is created. Required resources: guild, role.
        群组角色被创建时触发。必需资源：guild，role。
        """
        func._satori_event = 'guild-role-created'
        return func

    @staticmethod
    def guild_role_updated(func):
        """
        Triggered when a guild role is updated. Required resources: guild, role.
        群组角色被修改时触发。必需资源：guild，role。
        """
        func._satori_event = 'guild-role-updated'
        return func

    @staticmethod
    def guild_role_deleted(func):
        """
        Triggered when a guild role is deleted. Required resources: guild, role.
        群组角色被删除时触发。必需资源：guild，role。
        """
        func._satori_event = 'guild-role-deleted'
        return func

    # 内部接口
    @staticmethod
    def internal(target_event_type: str):
        """
        Triggered when a specified internal event is received, providing the name of the internal event type.
        当接收到指定内部事件时触发，需要提供内部事件类型的名称。
        """
        def decorator(func):
            func._satori_event = target_event_type
            return func
        return decorator

    @staticmethod
    def bot_start_up(func):
        """
        Decorator: Executes the function when the bot starts up.
        装饰器：在机器人启动时执行函数。
        no Args
        """
        func._startup = 'bot:start-up'
        return func

    @staticmethod
    def bot_event_built(func):
        """
        Decorator: Executes the function when the bot event is built.
        装饰器：在机器人事件构建完成后执行函数。
        Args (event)
        """
        func._event_built = 'bot:event-built'
        return func

    @staticmethod
    def bot_api_requested(func):
        """
        Decorator: Executes the function when the bot API is requested.
        装饰器：在机器人API请求完成后执行函数。
        Args (event, method, data, platform, self_id, response_dict)
        """
        func._api_requested = 'bot:api-requested'
        return func


on = On()

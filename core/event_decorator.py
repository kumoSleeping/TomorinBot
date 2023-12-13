from functools import wraps
from datetime import datetime
import time
from threading import Thread
import schedule

from bridge.session_adder import MessageExtension
# from load_plugins import function_info_list


class OnEvent:
    @staticmethod
    def message_created(func):
        '''
        当消息被创建时触发。必需资源：channel，message，user。
        '''
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
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
            inner_wrapper.enable_feature = True
            session = args[0]
            if session.type == 'guild-role-deleted':
                return func(session)

        return inner_wrapper


on_event = OnEvent()


from peewee import SqliteDatabase, Model, CharField, DateTimeField
from datetime import datetime
from datetime import timedelta
import inspect
from core import on, Event, config
from requests import Response
from plugins.schedule_do import interval_do

# 配置数据库 - 这里使用 SQLite
db = SqliteDatabase('plugins/analysis/analysis.db')


# 定义模型
class SessionReceive(Model):
    msg_type = CharField()
    text = CharField()
    channel_id = CharField()
    user_id = CharField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = db


# 定义模型
class SessionSend(Model):
    func = CharField()
    text = CharField()
    channel_id = CharField()
    self_id = CharField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = db


# 创建表
db.connect()
db.create_tables([SessionReceive], safe=True)
db.create_tables([SessionSend], safe=True)


@db.atomic()
def save_send_message(func, text, channel_id, self_id):
    """ 保存消息到数据库 """
    SessionSend.create(func=func, text=text, channel_id=channel_id, self_id=self_id)


@db.atomic()
def get_send_messages(limit=10, channel_id=None, self_id=None, func=None):
    """ 获取最近的发送几条消息 """
    if self_id is not None:
          if channel_id is None:
                if func is None:
                    # 限定了 self_id，但是没有限定 channel_id，也没有限定 func
                    return SessionSend.select().where(SessionSend.self_id == self_id).order_by(SessionSend.timestamp.desc()).limit(limit)
                else:
                    # 限定了 self_id，但是没有限定 channel_id，但是限定了 func
                    return SessionSend.select().where(SessionSend.self_id == self_id, SessionSend.func == func).order_by(SessionSend.timestamp.desc()).limit(limit)
          else:
                if func is None:
                    # 限定了 self_id，也限定了 channel_id，但是没有限定 func
                    return SessionSend.select().where(SessionSend.self_id == self_id, SessionSend.channel_id == channel_id).order_by(SessionSend.timestamp.desc()).limit(limit)
                else:
                    # 限定了 self_id，也限定了 channel_id，也限定了 func
                    return SessionSend.select().where(SessionSend.self_id == self_id, SessionSend.channel_id == channel_id, SessionSend.func == func).order_by(SessionSend.timestamp.desc()).limit(limit)
    else:
        if channel_id is None:
            if func is None:
                # 没有限定 self_id，也没有限定 channel_id，也没有限定 func
                return SessionSend.select().order_by(SessionSend.timestamp.desc()).limit(limit)
            else:
                # 没有限定 self_id，也没有限定 channel_id，但是限定了 func
                return SessionSend.select().where(SessionSend.func == func).order_by(SessionSend.timestamp.desc()).limit(limit)
        else:
            if func is None:
                # 没有限定 self_id，但是限定了 channel_id，也没有限定 func
                return SessionSend.select().where(SessionSend.channel_id == channel_id).order_by(SessionSend.timestamp.desc()).limit(limit)
            else:
                # 没有限定 self_id，但是限定了 channel_id，也限定了 func
                return SessionSend.select().where(SessionSend.channel_id == channel_id, SessionSend.func == func).order_by(SessionSend.timestamp.desc()).limit(limit)


@db.atomic()
def save_receive_message(msg_type, text, user_id, channel_id):
    """ 保存消息到数据库 """
    SessionReceive.create(msg_type=msg_type, text=text, user_id=user_id, channel_id=channel_id)


@db.atomic()
def get_receive_messages(limit=10, channel_id=None, user_id=None, msg_type=None):
    """ 获取最近的接收几条消息 """
    if user_id is not None:
          if channel_id is None:
                if msg_type is None:
                    # 限定了 user_id，但是没有限定 channel_id，也没有限定 msg_type
                    return SessionReceive.select().where(SessionReceive.user_id == user_id).order_by(SessionReceive.timestamp.desc()).limit(limit)
                else:
                    # 限定了 user_id，但是没有限定 channel_id，但是限定了 msg_type
                    return SessionReceive.select().where(SessionReceive.user_id == user_id, SessionReceive.msg_type == msg_type).order_by(SessionReceive.timestamp.desc()).limit(limit)
          else:
                if msg_type is None:
                    # 限定了 user_id，也限定了 channel_id，但是没有限定 msg_type
                    return SessionReceive.select().where(SessionReceive.user_id == user_id, SessionReceive.channel_id == channel_id).order_by(SessionReceive.timestamp.desc()).limit(limit)
                else:
                    # 限定了 user_id，也限定了 channel_id，也限定了 msg_type
                    return SessionReceive.select().where(SessionReceive.user_id == user_id, SessionReceive.channel_id == channel_id, SessionReceive.msg_type == msg_type).order_by(SessionReceive.timestamp.desc()).limit(limit)
    else:
        if channel_id is None:
            if msg_type is None:
                # 没有限定 user_id，也没有限定 channel_id，也没有限定 msg_type
                return SessionReceive.select().order_by(SessionReceive.timestamp.desc()).limit(limit)
            else:
                # 没有限定 user_id，也没有限定 channel_id，但是限定了 msg_type
                return SessionReceive.select().where(SessionReceive.msg_type == msg_type).order_by(SessionReceive.timestamp.desc()).limit(limit)
        else:
            if msg_type is None:
                # 没有限定 user_id，但是限定了 channel_id，也没有限定 msg_type
                return SessionReceive.select().where(SessionReceive.channel_id == channel_id).order_by(SessionReceive.timestamp.desc()).limit(limit)
            else:
                # 没有限定 user_id，但是限定了 channel_id，也限定了 msg_type
                return SessionReceive.select().where(SessionReceive.channel_id == channel_id, SessionReceive.msg_type == msg_type).order_by(SessionReceive.timestamp.desc()).limit(limit)


@db.atomic()
def delete_old_records(model, hours_ago):
    # 计算过期时间
    expiry_time = datetime.now() - timedelta(hours=hours_ago)

    # 构建并执行删除查询
    query = model.delete().where(model.timestamp < expiry_time)
    deleted_count = query.execute()
    print(f"[database] Deleted {deleted_count} records from {model.__name__}")


@interval_do(1*60*60)
def delete_old_records_():
    """ 删除过期的记录 """
    delete_old_records(SessionReceive, 24)
    delete_old_records(SessionSend, 24)


delete_old_records_()


@on.after_request
def save_send(event: Event, method: str, data: dict, platform: str, self_id: str, response: Response):
    """ 保存发送的消息 """
    try:
        # 调用堆栈
        stack_info = inspect.stack()
        plugin_functions = []
        for index, frame in enumerate(stack_info):
            # 检查文件名是否符合条件（在 'plugins' 目录下的 '__init__.py'）
            if 'plugins' in frame.filename and '__init__.py' in frame.filename:
                # 添加函数名和序号
                plugin_functions.append((index, frame.function))
        # 获取调用函数名
        # print('func', plugin_functions[-1])
        func = plugin_functions[-1][1]
        save_send_message(func, data.get('content'), data.get('channel_id'), self_id)
    except:
        print(f'[database] 无法保存发送的消息')
    return event, method, data, platform, self_id, response


@on.after_event
def save_receive(event: Event):
    """ 保存接收到的消息 """
    try:
        save_receive_message(event.type, event.message.content, event.user.id, event.channel.id)
    except:
        print(f'[database] 无法保存接收到的消息')
    return event









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
class EventReceive(Model):
    msg_type = CharField()
    text = CharField()
    channel_id = CharField()
    user_id = CharField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = db


# 定义模型
class EventSend(Model):
    text = CharField()
    channel_id = CharField()
    self_id = CharField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = db


# 创建表
db.connect()
db.create_tables([EventReceive], safe=True)
db.create_tables([EventSend], safe=True)


@db.atomic()
def save_send_message(text, channel_id, self_id):
    """ 保存消息到数据库 """
    EventSend.create(text=text, channel_id=channel_id, self_id=self_id)


@db.atomic()
def get_send_messages(limit=10, channel_id=None, self_id=None):
    """ 获取最近的发送几条消息 """
    if self_id is not None:
          if channel_id is None:
               # 限定了 self_id，但是没有限定 channel_id
                return EventSend.select().where(EventSend.self_id == self_id).order_by(EventSend.timestamp.desc()).limit(limit)
          else:
                # 限定了 self_id，也限定了 channel_id
                return EventSend.select().where(EventSend.self_id == self_id, EventSend.channel_id == channel_id).order_by(EventSend.timestamp.desc()).limit(limit)
    else:
        if channel_id is None:
            # 没有限定 self_id，也没有限定 channel_id
            return EventSend.select().order_by(EventSend.timestamp.desc()).limit(limit)
        else:
            # 没有限定 self_id，但是限定了 channel_id
            return EventSend.select().where(EventSend.channel_id == channel_id).order_by(EventSend.timestamp.desc()).limit(limit)

@db.atomic()
def save_receive_message(msg_type, text, user_id, channel_id):
    """ 保存消息到数据库 """
    EventReceive.create(msg_type=msg_type, text=text, user_id=user_id, channel_id=channel_id)


@db.atomic()
def get_receive_messages(limit=10, channel_id=None, user_id=None, msg_type=None):
    """ 获取最近的接收几条消息 """
    if user_id is not None:
          if channel_id is None:
                if msg_type is None:
                    # 限定了 user_id，但是没有限定 channel_id，也没有限定 msg_type
                    return EventReceive.select().where(EventReceive.user_id == user_id).order_by(EventReceive.timestamp.desc()).limit(limit)
                else:
                    # 限定了 user_id，但是没有限定 channel_id，但是限定了 msg_type
                    return EventReceive.select().where(EventReceive.user_id == user_id, EventReceive.msg_type == msg_type).order_by(EventReceive.timestamp.desc()).limit(limit)
          else:
                if msg_type is None:
                    # 限定了 user_id，也限定了 channel_id，但是没有限定 msg_type
                    return EventReceive.select().where(EventReceive.user_id == user_id, EventReceive.channel_id == channel_id).order_by(EventReceive.timestamp.desc()).limit(limit)
                else:
                    # 限定了 user_id，也限定了 channel_id，也限定了 msg_type
                    return EventReceive.select().where(EventReceive.user_id == user_id, EventReceive.channel_id == channel_id, EventReceive.msg_type == msg_type).order_by(EventReceive.timestamp.desc()).limit(limit)
    else:
        if channel_id is None:
            if msg_type is None:
                # 没有限定 user_id，也没有限定 channel_id，也没有限定 msg_type
                return EventReceive.select().order_by(EventReceive.timestamp.desc()).limit(limit)
            else:
                # 没有限定 user_id，也没有限定 channel_id，但是限定了 msg_type
                return EventReceive.select().where(EventReceive.msg_type == msg_type).order_by(EventReceive.timestamp.desc()).limit(limit)
        else:
            if msg_type is None:
                # 没有限定 user_id，但是限定了 channel_id，也没有限定 msg_type
                return EventReceive.select().where(EventReceive.channel_id == channel_id).order_by(EventReceive.timestamp.desc()).limit(limit)
            else:
                # 没有限定 user_id，但是限定了 channel_id，也限定了 msg_type
                return EventReceive.select().where(EventReceive.channel_id == channel_id, EventReceive.msg_type == msg_type).order_by(EventReceive.timestamp.desc()).limit(limit)


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
    delete_old_records(EventReceive, 24)
    delete_old_records(EventSend, 24)


delete_old_records_()


@on.after_request
def save_send(event: Event, method: str, data: dict, platform: str, self_id: str, response: Response):
    """ 保存发送的消息 """
    try:
        save_send_message(data.get('content'), data.get('channel_id'), self_id)
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









import re

from bridge.tomorin import on_event, on_activator, new_api


bot_self_id = 'x'
bdb_channel_id = 'xx'
bdb_platform = 'xxx'
bd_self_id = 'xxxxx'


@on_event.message_created
def auto_bdb(session):
    """
    全自动笨蛋读博机
    每天会间隔70min发送一条消息 笨蛋补助
    并根据回复的消息自动投币
    """
    # 保证发消息者是笨蛋，被quote者是bot
    if session.user.id != bd_self_id or session.message.quote.user.id != bot_self_id:
        return
    msg: str = session.message.content
    # 你现在不许玩了！还要 4分8秒 之后才能玩笨蛋机哦 ！
    if msg.startswith('你现在不许玩了！') and msg.endswith('之后才能玩笨蛋机哦 ！'):
        return  # 不处理
    # 您当前拥有 263921 个笨蛋(>= 15 )， 不符合领取条件。 / 12 个笨蛋已经加入您的账户(冷却 4 小时)
    if (msg.startswith('您当前拥有') and msg.endswith('不符合领取条件。') or
    msg.endswith('个笨蛋已经加入您的账户(冷却 4 小时)') or
    msg.startswith('你现在不许玩笨蛋机！')):
        num = re.findall(r"\d+\.?\d*", msg)
        # 小于1000 直接梭哈
        if int(num[0]) <= 1000:
            session.send(f'投币{num[0]}')
            return
        # 大于1000 投币 1 / 5
        num = int(num[0]) // 5  # 数字 / 5 取整
        session.send(f'投币{num}')
        return
    if msg.endswith('后才能领取笨蛋补助!') or msg.startswith('出错了！'):
        session.send(f'投币1000000000000000000000000000')


# 每天定时发消息，每70分钟一次
@on_activator.timer(['00:00', '01:10', '02:20', '03:30', '04:40', '05:50', '07:00', '08:10', '09:20', '10:30', '11:40', '12:50', '14:00', '15:10', '16:20', '17:30', '18:40', '19:50', '21:00', '22:10', '23:20'])
def clock1():
   new_api_1 = new_api(bdb_platform, bot_self_id)
   new_api_1.message_create(channel_id=bdb_channel_id, content=f'笨蛋补助')





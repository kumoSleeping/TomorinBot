from bridge.tomorin import h, rm_1_at, new_api


def forward(session):
    """
    用户Bob发言时，转发到特定频道
    """
    if session.user.id == 'Bob_id' and session.platform == 'sb_tx':
        if session.channel.id != 'xxx':
            new_api_1 = new_api(platform='sb_tx', self_id='bot_id')
            new_api_1.message_create('xxx', f"[{session.channel.name}]" + "Bob:" + session.message.content)





from bridge.tomorin import on_event, on_activator, admin_list, h


@on_activator.command('echo')
def echo(session):
    """
    回声
    复读你的话
    """
    if session.command.args and session.user.id in admin_list:
        # session.message_create(content=session.command.text)
        session.send(session.command.text)


@on_event.message_created
def echo2(session):
    """
    回声2
    复读你的话
    """
    if session.message.content.startswith('echo ') and session.user.id in admin_list:
        session.send(session.message.content[5:])


@on_activator.command('koishi')
def koishi(session):
    """
    发送koishi的logo
    """
    if not session.command.args:
        session.send(h.image('https://koishi.chat/logo.png'))


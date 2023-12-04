
from core.tomorin import on_event, on_activator


@on_activator.command('复读')
def echo(session):
    """
    回声
    复读你的话
    """
    print(session.data)
    if session.command.args:
        # session.message_create(content=session.command.text)
        session.send(session.command.text)


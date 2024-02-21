from core import Event, on


@on.message_created
def echo(event: Event):
    print(event.message.content)

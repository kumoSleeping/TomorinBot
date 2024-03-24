from mods import on, Event, match_command


@on.message_created
def echo_message_created(event: Event):
    if res:=match_command(event, 'echo'):
        res.send(res.text)
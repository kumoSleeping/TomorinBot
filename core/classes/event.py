from core.transmit.api import call_api
from satori import Event as SatoriEvent


class Event(SatoriEvent):
    def message_create(self, content: str = None, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return call_api(event=self, method='message.create', data={
            'channel_id': channel_id,
            'content': content,
        }, platform=self.platform, self_id=self.self_id)

    def message_delete(self, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return call_api(event=self, method='message.delete', data={
            'channel_id': channel_id,
            'message_id': message_id,
        }, platform=self.platform, self_id=self.self_id)

    def message_update(self, content: str = None, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return call_api(event=self, method='message.update', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'content': content,
        }, platform=self.platform, self_id=self.self_id)

    def message_list(self, next_token: str = None, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return call_api(event=self, method='message.list', data={
            'channel_id': channel_id,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def channel_get(self, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return call_api(event=self, method='channel.get', data={
            'channel_id': channel_id,
        }, platform=self.platform, self_id=self.self_id)

    def channel_list(self, next_token: str = None, guild_id: str = None):
        guild_id = guild_id or self.guild.id
        return call_api(event=self, method='channel.list', data={
            'guild_id': guild_id,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def channel_create(self, channel_data: dict = None, guild_id: str = None):
        guild_id = guild_id or self.guild.id
        return call_api(event=self, method='channel.create', data={
            'guild_id': guild_id,
            'data': channel_data,
        }, platform=self.platform, self_id=self.self_id)

    def channel_update(self, channel_data: dict = None, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return call_api(event=self, method='channel.update', data={
            'channel_id': channel_id,
            'data': channel_data,
        }, platform=self.platform, self_id=self.self_id)

    def channel_delete(self, channel_id: str = None):
        channel_id = channel_id or self.channel.id
        return call_api(event=self, method='channel.delete', data={
            'channel_id': channel_id,
        }, platform=self.platform, self_id=self.self_id)

    def guild_get(self, guild_id: str = None):
        guild_id = guild_id or self.guild.id
        return call_api(event=self, method='guild.get', data={
            'guild_id': guild_id,
        }, platform=self.platform, self_id=self.self_id)

    def guild_list(self, next_token: str = None):
        return call_api(event=self, method='guild.list', data={
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def guild_approve(self, approve: bool = False, comment: str = None, message_id: str = None):
        message_id = message_id or self.message.id
        return call_api(event=self, method='guild.approve', data={
            'message_id': message_id,
            'approve': approve,
            'comment': comment,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_get(self, guild_id: str = None, user_id: str = None):
        guild_id = guild_id or self.guild.id
        user_id = user_id or self.user.id
        return call_api(event=self, method='guild.member.get', data={
            'guild_id': guild_id,
            'user_id': user_id,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_list(self, next_token: str = None, guild_id: str = None):
        guild_id = guild_id or self.guild.id
        return call_api(event=self, method='guild.member.list', data={
            'guild_id': guild_id,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_kick(self, permanent: bool = False, guild_id: str = None, user_id: str = None):
        guild_id = guild_id or self.guild.id
        user_id = user_id or self.user.id
        return call_api(event=self, method='guild.member.kick', data={
            'guild_id': guild_id,
            'user_id': user_id,
            'permanent': permanent,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_approve(self, approve: bool = False, comment: str = None, message_id: str = None):
        message_id = message_id or self.message.id
        return call_api(event=self, method='guild.member.approve', data={
            'message_id': message_id,
            'approve': approve,
            'comment': comment,
        }, platform=self.platform, self_id=self.self_id)

    def login_get(self):
        return call_api(event=self, method='login.get', data={}, platform=self.platform, self_id=self.self_id)

    def user_get(self, user_id: str = None):
        user_id = user_id or self.user.id
        return call_api(event=self, method='user.get', data={
            'user_id': user_id,
        }, platform=self.platform, self_id=self.self_id)

    def friend_list(self, next_token: str = None):
        return call_api(event=self, method='friend.list', data={
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def friend_approve(self, approve: bool = False, comment: str = None, message_id: str = None):
        message_id = message_id or self.message.id
        return call_api(event=self, method='friend.approve', data={
            'message_id': message_id,
            'approve': approve,
            'comment': comment,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_create(self, emoji: str = None, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return call_api(event=self, method='reaction.create', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_delete(self, emoji: str = None, user_id: str = None, channel_id: str = None, message_id: str = None):
        user_id = user_id or self.user.id
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return call_api(event=self, method='reaction.delete', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
            'user_id': user_id,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_clear(self, emoji: str = None, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return call_api(event=self, method='reaction.clear', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_list(self, emoji: str = None, next_token: str = None, channel_id: str = None, message_id: str = None):
        channel_id = channel_id or self.channel.id
        message_id = message_id or self.message.id
        return call_api(event=self, method='reaction.list', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def internal_event_create(self, data: dict, internal_method: str = None):
        if internal_method is None:
            internal_method = self._type
        return call_api(event=self, method=internal_method, data=data, platform=self.platform, self_id=self.self_id, internal=True)

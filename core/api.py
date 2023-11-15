from api_request import send_request


class Api:
    def __init__(self, platform, self_id):
        self.platform = platform
        self.self_id = self_id

    # message
    def message_create(self, channel_id: str, content: str):
        return send_request(method='message.create', data={
            'channel_id': channel_id,
            'content': content,
        }, platform=self.platform, self_id=self.self_id)

    def message_get(self, channel_id: str, message_id: str):
        return send_request(method='message.get', data={
            'channel_id': channel_id,
            'message_id': message_id,
        }, platform=self.platform, self_id=self.self_id)

    def message_delete(self, channel_id: str, message_id: str):
        return send_request(method='message.delete', data={
            'channel_id': channel_id,
            'message_id': message_id,
        }, platform=self.platform, self_id=self.self_id)

    def message_update(self, channel_id: str, message_id: str, content: str):
        return send_request(method='message.update', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'content': content,
        }, platform=self.platform, self_id=self.self_id)

    def message_list(self, channel_id: str, next_token: str):
        return send_request(method='message.list', data={
            'channel_id': channel_id,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def channel_get(self, channel_id: str):
        return send_request(method='channel.get', data={
            'channel_id': channel_id,
        }, platform=self.platform, self_id=self.self_id)

    # channel
    def channel_list(self, guild_id: str, next_token: str):
        return send_request(method='channel.list', data={
            'guild_id': guild_id,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def channel_create(self, guild_id: str, channel_data: dict):
        return send_request(method='channel.create', data={
            'guild_id': guild_id,
            'data': channel_data,
        }, platform=self.platform, self_id=self.self_id)

    def channel_update(self, channel_id: str, channel_data: dict):
        return send_request(method='channel.update', data={
            'channel_id': channel_id,
            'data': channel_data,
        }, platform=self.platform, self_id=self.self_id)

    def channel_delete(self, channel_id: str):
        return send_request(method='channel.delete', data={
            'channel_id': channel_id,
        }, platform=self.platform, self_id=self.self_id)

    def user_channel_create(self, user_id: str, guild_id: str):
        return send_request(method='user.channel.create', data={
            'user_id': user_id,
            'guild_id': guild_id,
        }, platform=self.platform, self_id=self.self_id)

    def guild_get(self, guild_id: str):
        return send_request(method='guild.get', data={
            'guild_id': guild_id,
        }, platform=self.platform, self_id=self.self_id)

    def guild_list(self, next_token: str):
        return send_request(method='guild.list', data={
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def guild_approve(self, message_id: str, approve: bool, comment: str):
        return send_request(method='guild.approve', data={
            'message_id': message_id,
            'approve': approve,
            'comment': comment,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_get(self, guild_id: str, user_id: str):
        return send_request(method='guild.member.get', data={
            'guild_id': guild_id,
            'user_id': user_id,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_list(self, guild_id: str, next_token: str):
        return send_request(method='guild.member.list', data={
            'guild_id': guild_id,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_kick(self, guild_id: str, user_id: str, permanent: bool):
        return send_request(method='guild.member.kick', data={
            'guild_id': guild_id,
            'user_id': user_id,
            'permanent': permanent,
        }, platform=self.platform, self_id=self.self_id)

    def guild_member_approve(self, message_id: str, approve: bool, comment: str):
        return send_request(method='guild.member.approve', data={
            'message_id': message_id,
            'approve': approve,
            'comment': comment,
        }, platform=self.platform, self_id=self.self_id)

    # login
    def login_get(self):
        return send_request(method='login.get', data={}, platform=self.platform, self_id=self.self_id)

    # user
    def user_get(self, user_id: str):
        return send_request(method='user.get', data={
            'user_id': user_id,
        }, platform=self.platform, self_id=self.self_id)

    def friend_list(self, next_token: str):
        return send_request(method='friend.list', data={
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)

    def friend_approve(self, message_id: str, approve: bool, comment: str):
        return send_request(method='friend.approve', data={
            'message_id': message_id,
            'approve': approve,
            'comment': comment,
        }, platform=self.platform, self_id=self.self_id)

    # reaction
    def reaction_create(self, channel_id: str, message_id: str, emoji: str):
        return send_request(method='reaction.create', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_delete(self, channel_id: str, message_id: str, emoji: str, user_id: str):
        return send_request(method='reaction.delete', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
            'user_id': user_id,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_clear(self, channel_id: str, message_id: str, emoji: str):
        return send_request(method='reaction.clear', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
        }, platform=self.platform, self_id=self.self_id)

    def reaction_list(self, channel_id: str, message_id: str, emoji: str, next_token: str):
        return send_request(method='reaction.list', data={
            'channel_id': channel_id,
            'message_id': message_id,
            'emoji': emoji,
            'next': next_token,
        }, platform=self.platform, self_id=self.self_id)


def api(platform, self_id):
    return Api(platform=platform, self_id=self_id)

from core import config

if 'auth' not in config:
    config['auth'] = []


def is_admin(platform, user_id):
    for auth in config['auth']:
        if auth['platform'] == platform:
            if str(user_id) in auth['admin']:
                return True
    return False



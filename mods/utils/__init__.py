import os
import inspect
from mods import config


config.need('auth', [
        {
          "platform": "red",
          "admin": [
            "114514"
          ]
        },
        {
          "platform": "chronocat",
          "admin": [
            "114514"
          ]
        }
      ])


# Create the 'assets' directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')


def is_admin(platform, user_id):
    '''
    实现根据配置文件，判断是否 admin
    '''
    for auth in config.get_key('auth'):
        if auth['platform'] == platform:
            if str(user_id) in auth['admin']:
                return True
    return False








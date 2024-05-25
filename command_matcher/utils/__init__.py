from core.interfaces import config


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


def is_admin(platform: str, user_id: str):
    '''
    实现根据配置文件，判断是否 admin
    '''
    for auth in config.get_key('auth'):
        if auth['platform'] == platform:
            if user_id in auth['admin']:
                return True
    return False







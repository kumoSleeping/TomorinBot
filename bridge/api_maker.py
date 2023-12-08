from core.api import Api


def new_api(platform, self_id):
    return Api(platform=platform, self_id=self_id)
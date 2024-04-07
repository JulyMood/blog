from app.dao.base_dao import get_redis
import json

EXPIRE = 60 * 60 * 2


def save_token(token, user_info):
    get_redis().setex(token, EXPIRE, json.dumps(user_info))


def get_token(token):
    return get_redis().get(token)

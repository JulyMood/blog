from app.dao import user_info, token_redis
import uuid
import bcrypt


def login(username, password):
    userinfo = user_info.login(username)
    if not userinfo or not bcrypt.checkpw(password.encode('utf-8'), userinfo.password):
        return False
    token = uuid.uuid4().hex
    token_redis.save_token(token, {'id': userinfo.id, 'username': userinfo.username, 'role': userinfo.role})
    return token


def register(email, username, password):
    if user_info.get(username):
        return '用户名已被注册'
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_info.register(email, username, password)
    return True


def check_token(token):
    return token_redis.get_token(token)

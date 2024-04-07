from datetime import datetime

from app.dao import article, comments
from app.services import rag_service
import pandas as pd


def query_article(page_no=1):
    page_size = 10
    offset = (page_no - 1) * page_size
    data, total = article.query(offset, page_size)
    for row in data:
        row.create_time = row.create_time.strftime('%Y-%m-%d %H:%M:%S')
    return data, int(total / page_size) + 1 if total > page_size else 1


def create_article(title, type, content, create_time=None):
    try:
        article.create(title, type, content, create_time)
        # 插入向量数据库
        rag_service.add_text(content)
        return True
    except Exception as e:
        return e.__str__()


def delete_article(_id):
    try:
        article.delete(_id)
        return True
    except Exception as e:
        return e.__str__()


def update_article(_id, title, type, content):
    try:
        return article.update(_id, title, type, content) == 1
    except Exception as e:
        return e.__str__()


def like_article(_id):
    article.likes(_id)


def add_comments(user_id, username, article_id, content):
    comments.create(user_id, username, article_id, content)


def del_comments(_id):
    comments.delete(_id)


def get_recommendation():
    return article.get_recommendation()


def statistics():
    _list = article.all()
    if len(_list) == 0:
        return None, None
    data = [{k: v for k, v in obj.__dict__.items() if not k.startswith('_')} for obj in _list]
    df = pd.DataFrame(data)
    df['create_time'] = pd.to_datetime(df['create_time']).dt.date
    time_group = df.groupby('create_time').size()
    type_group = df.groupby('type').size()
    return time_group, type_group

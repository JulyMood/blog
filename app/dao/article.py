from datetime import datetime

from sqlalchemy import Integer, String, Column, DateTime, func, Text
from sqlalchemy.orm import relationship, joinedload

from app.dao.base_dao import Base, session_scope, engine


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, unique=True, comment='标题')
    type = Column(String(50), nullable=True, comment='类型')
    content = Column(Text, nullable=False, comment='内容')
    like_count = Column(Integer, nullable=False, server_default='0', comment='点赞数')
    create_time = Column(DateTime, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.current_timestamp(), onupdate=datetime.now, comment='修改时间')

    comments = relationship('Comments', back_populates='article', cascade='all, delete')


Base.metadata.create_all(engine)


def create(title, type, content, create_time=None):
    article = Article(title=title, type=type, content=content, create_time=create_time)
    with session_scope() as session:
        session.add(article)


def query(offset, limit):
    with session_scope() as session:
        _query = session.query(Article)
        data = _query.options(joinedload(Article.comments)).order_by(Article.create_time.desc()).offset(offset).limit(
            limit).all()
        total = _query.with_entities(func.count(Article.id)).scalar()
        return data, total


def update(_id, title, type, content):
    with session_scope() as session:
        return session.query(Article).filter(Article.id == _id).update(
            {'title': title, 'type': type, 'content': content})


def delete(_id):
    with session_scope() as session:
        session.delete(session.get(Article, _id))


def likes(_id):
    with session_scope() as session:
        return session.query(Article).filter(Article.id == _id).update({Article.like_count: Article.like_count + 1})


def get_recommendation():
    with session_scope() as session:
        return session.query(Article).order_by(Article.like_count.desc()).limit(5).all()


def all():
    with session_scope() as session:
        return session.query(Article).all()

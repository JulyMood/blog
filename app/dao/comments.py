from sqlalchemy import Integer, Column, DateTime, func, Text, ForeignKey, String
from sqlalchemy.orm import relationship
from app.dao.base_dao import Base, session_scope, engine


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_info.id'), nullable=True, comment='关联用户ID, 可为空')
    username = Column(String(50), nullable=True, comment='用户名称')
    article_id = Column(Integer, ForeignKey('article.id'), nullable=False, comment='关联文章ID')
    content = Column(Text, nullable=False, comment='评论内容')
    create_time = Column(DateTime, server_default=func.current_timestamp(), comment='创建时间')

    article = relationship('Article', back_populates='comments')


Base.metadata.create_all(engine)


def create(user_id, username, article_id, content):
    comments = Comments(user_id=user_id, username=username, article_id=article_id, content=content)
    with session_scope() as session:
        session.add(comments)


def delete(_id):
    with session_scope() as session:
        session.delete(session.get(Comments, _id))


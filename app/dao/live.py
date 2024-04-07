from sqlalchemy import Integer, Column, DateTime, func, Text, String
from app.dao.base_dao import Base, session_scope, engine


class Live(Base):
    __tablename__ = 'live'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False, comment='详细内容')
    media_url = Column(String(200), nullable=False, comment='视频或图片')
    caption = Column(String(50), nullable=True, comment='media标题')
    like_count = Column(Integer, nullable=False, server_default='0', comment='点赞数')
    create_time = Column(DateTime, server_default=func.current_timestamp(), comment='创建时间')


Base.metadata.create_all(engine)


def create(content, media_url, caption):
    article = Live(content=content, media_url=media_url, caption=caption)
    with session_scope() as session:
        session.add(article)


def query():
    with session_scope() as session:
        return session.query(Live).all()

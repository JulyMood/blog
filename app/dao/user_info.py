from sqlalchemy import Integer, String, Column, DateTime, func, Boolean
from app.dao.base_dao import Base, session_scope, engine


class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True, comment='用户名')
    password = Column(String(72), nullable=False, comment='密码')
    email = Column(String(50), nullable=False, unique=True, comment='邮箱')
    role = Column(String(50), nullable=False, server_default='user', comment='角色')
    valid = Column(Boolean, nullable=False, default=True, comment='有效性')
    create_time = Column(DateTime, server_default=func.current_timestamp(), comment='创建时间')


Base.metadata.create_all(engine)


def register(email, username, password):
    user = UserInfo(username=username, password=password, email=email)
    with session_scope() as session:
        session.add(user)


def login(username):
    with session_scope() as session:
        return session.query(UserInfo).filter(
            UserInfo.username == username, UserInfo.valid == True).first()


def get(username):
    with session_scope() as session:
        return session.query(UserInfo).filter(UserInfo.username == username, UserInfo.valid == True).first()

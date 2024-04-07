from app.config import conf
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import redis

engine = create_engine(conf.sqlite.url, echo=True, pool_recycle=300)
Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


redis_pool = redis.ConnectionPool(**conf.redis.__dict__)


def get_redis():
    return redis.Redis(connection_pool=redis_pool)

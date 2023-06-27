from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .config import env

engine = create_engine(env.database_uri, echo=env.debug_mode)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Iterator[scoped_session[Session]]:
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()

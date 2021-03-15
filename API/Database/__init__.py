import sqlalchemy
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

from API import find_subclasses

SQLALCHEMY_DATABASE_URL = config("sql_db_url")

engine = None


if "sqlite" in str(SQLALCHEMY_DATABASE_URL).lower():
    engine = sqlalchemy.create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = create_session(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

find_subclasses("API.Database.Models")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()

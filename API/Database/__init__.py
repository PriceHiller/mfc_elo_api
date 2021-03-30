import os
import sqlalchemy

from databases import Database

from API import config

from API.Database.Models import ModelBase
from API.Database.Models import metadata


class BaseDB:
    SQLALCHEMY_DATABASE_URL = config.get("sql_db_url")

    if not SQLALCHEMY_DATABASE_URL:
        raise AttributeError(f"SQLALCHEMY_DATABASE_URL does not have an environment variable: \"sql_db_url\"")

    db = Database(SQLALCHEMY_DATABASE_URL)

    @classmethod
    def create_tables(cls):
        engine = sqlalchemy.create_engine(cls.SQLALCHEMY_DATABASE_URL)
        engine.execute(r'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        metadata.create_all(engine)
        for subclass in ModelBase.__subclasses__():
            subclass.metadata.create_all(engine)

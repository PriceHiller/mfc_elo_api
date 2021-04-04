import sqlalchemy
import databases

from databases import Database

from API import config

from API.Database.Models import ModelBase
from API.Database.Models import metadata


class BaseDB:
    SQLALCHEMY_DATABASE_URL = config("SQL_DB_URL", cast=databases.DatabaseURL)

    if not SQLALCHEMY_DATABASE_URL:
        raise AttributeError(f"SQLALCHEMY_DATABASE_URL does not have an environment variable: \"sql_db_url\"")

    db = Database(str(SQLALCHEMY_DATABASE_URL))

    @classmethod
    def create_tables(cls):
        engine = sqlalchemy.create_engine(str(cls.SQLALCHEMY_DATABASE_URL))
        engine.execute(r'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        metadata.create_all(engine)
        for subclass in ModelBase.__subclasses__():
            subclass.metadata.create_all(engine)

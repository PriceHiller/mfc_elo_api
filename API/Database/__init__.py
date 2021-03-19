from decouple import config
from databases import Database

from API.Database.Models import metadata


class BaseDB:
    SQLALCHEMY_DATABASE_URL = config("sql_db_url")

    db = Database(SQLALCHEMY_DATABASE_URL)

    @classmethod
    async def create_tables(cls):
        await cls.db.execute(metadata.create_all())

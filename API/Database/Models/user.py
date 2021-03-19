import sqlalchemy

from . import ModelBase
from . import AlcBase


class User(ModelBase, AlcBase):
    __table__: sqlalchemy.Table

    __tablename__ = "users"

    username = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

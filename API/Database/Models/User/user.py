import sqlalchemy

from sqlalchemy.orm import relationship

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase

from .tokens import Token
class User(ModelBase, AlcBase):
    __tablename__ = "users"

    username = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True, nullable=False)
    relationship(Token, cascade="all, delete", passive_deletes=True)

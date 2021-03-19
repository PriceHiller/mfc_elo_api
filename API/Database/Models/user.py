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

Meta = User.metadata

__all__ = [
    "User",
    "Meta"
]

# __table__ = \
#         sqlalchemy.Table(
#             "users",
#             metadata,
#             sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#             sqlalchemy.Column("username", sqlalchemy.String, unique=True),
#             sqlalchemy.Column("hashed_password", sqlalchemy.String),
#             sqlalchemy.Column("email", sqlalchemy.Integer, unique=True, index=True),
#             sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=True)
#

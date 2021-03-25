import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase


class Token(ModelBase, AlcBase):
    __tablename__ = "tokens"

    token = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    user_id = sqlalchemy.Column(UUID, sqlalchemy.ForeignKey("users.id", ondelete="cascade"), index=True)

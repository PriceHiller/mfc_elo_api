import sqlalchemy

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase


class DiscordID(ModelBase, AlcBase):
    discord_id = sqlalchemy.Column(
        sqlalchemy.String,
        index=True,
    )


class Permission(ModelBase, AlcBase):
    permission_col = sqlalchemy.Column(
        sqlalchemy.JSON,
        nullable=True
    )

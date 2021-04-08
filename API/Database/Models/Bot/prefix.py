import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase


class Prefix(ModelBase, AlcBase):
    __tablename__ = "discord_prefix"

    prefix = sqlalchemy.Column(
        sqlalchemy.String,
        index=True,
        unique=False,
        nullable=False
    )
    guild_id = sqlalchemy.Column(
        UUID,
        sqlalchemy.ForeignKey("discord_guild.id"),
        unique=True,
        nullable=False
    )

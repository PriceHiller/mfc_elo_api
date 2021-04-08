import sqlalchemy

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase
from API.Database.Models.Bot import DiscordID
from API.Database.Models.Bot import Permission


class Role(ModelBase, AlcBase, DiscordID, Permission):
    __tablename__ = "discord_guild"

    guild_id = sqlalchemy.Column(
        sqlalchemy.String,
        sqlalchemy.ForeignKey("discord_guild.id"),
        unique=True,
        nullable=False
    )

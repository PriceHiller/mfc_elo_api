import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase
from API.Database.Models.Bot import DiscordID
from API.Database.Models.Bot import PermissionJSON


class Role(ModelBase, AlcBase, DiscordID, PermissionJSON):
    __tablename__ = "discord_role"

    guild_id = sqlalchemy.Column(
        UUID,
        sqlalchemy.ForeignKey("discord_guild.id"),
        unique=True,
        nullable=False
    )
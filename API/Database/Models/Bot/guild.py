import sqlalchemy

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase
from API.Database.Models.Bot import DiscordID


class Guild(ModelBase, AlcBase, DiscordID):
    __tablename__ = "discord_guild"

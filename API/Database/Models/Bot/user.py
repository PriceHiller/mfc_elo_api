import sqlalchemy

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase
from API.Database.Models.Bot import DiscordID
from API.Database.Models.Bot import PermissionJSON


class User(ModelBase, AlcBase, DiscordID, PermissionJSON):
    __tablename__ = "discord_user"

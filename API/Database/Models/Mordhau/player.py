import sqlalchemy

from sqlalchemy.dialects.postgresql import UUID
from API.Database.Models import ModelBase
from API.Database.Models import AlcBase


class Player(ModelBase, AlcBase):
    __tablename__ = "mfc_players"

    player_name = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)
    playfab_id = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True, nullable=False)
    steam_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)
    team_id = sqlalchemy.Column(UUID, sqlalchemy.ForeignKey("mfc_teams.id"))

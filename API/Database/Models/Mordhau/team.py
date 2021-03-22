import sqlalchemy

from sqlalchemy.orm import relationship

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase


class Team(ModelBase, AlcBase):
    __tablename__ = "mfc_teams"

    team_name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    elo = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    player = relationship("mfc_players")

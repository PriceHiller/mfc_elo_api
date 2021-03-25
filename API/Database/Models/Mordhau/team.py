import sqlalchemy

from sqlalchemy.orm import relationship

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase

# Important, see the player relationship. This binds it.
from .player import Player


class Team(ModelBase, AlcBase):
    __tablename__ = "mfc_teams"

    team_name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    elo = sqlalchemy.Column(sqlalchemy.Integer
                            , index=True, nullable=False)
    player = relationship(Player, cascade="all")
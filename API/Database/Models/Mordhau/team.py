import sqlalchemy

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase


class Team(ModelBase, AlcBase):
    __tablename__ = "mfc_teams"

    team_name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    elo = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=False)
    player = relationship("mfc_players", cascade="all")

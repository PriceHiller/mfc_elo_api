import sqlalchemy

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase

# Important, see the player relationship. This binds it.
from .player import Player


class Team(ModelBase, AlcBase):
    __tablename__ = "mfc_teams"

    team_name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    elo = sqlalchemy.Column(sqlalchemy.Integer
                            , index=True, nullable=False)
    discord_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, index=True, nullable=True)
    ambassador = sqlalchemy.Column(
        UUID,
        sqlalchemy.ForeignKey("mfc_players.id"),
        nullable=True,
        index=True
    )
    player = relationship(Player, cascade="all")

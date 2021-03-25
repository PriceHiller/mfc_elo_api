import sqlalchemy

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase


class RoundPlayers(ModelBase, AlcBase):
    __tablename__ = "mfc_round_players"

    kills = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    deaths = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    assists = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    team = sqlalchemy.Column(
        UUID,
        sqlalchemy.ForeignKey("mfc_teams.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    player_id = sqlalchemy.Column(UUID, sqlalchemy.ForeignKey("mfc_players.id", ondelete="SET NULL"))
    round_id = sqlalchemy.Column(UUID, sqlalchemy.ForeignKey("mfc_rounds.id", ondelete="CASCADE"), index=True)


class Round(ModelBase, AlcBase):
    __tablename__ = "mfc_rounds"

    team1_win = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    team2_win = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    set_id = sqlalchemy.Column(UUID, sqlalchemy.ForeignKey("mfc_sets.id", ondelete="CASCADE"), index=True)
    round_players = relationship(RoundPlayers, cascade="all, delete", passive_deletes=True)

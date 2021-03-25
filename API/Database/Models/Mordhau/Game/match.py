import sqlalchemy

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase

from .set import Set


class Match(ModelBase, AlcBase):
    __tablename__ = "mfc_matches"

    team1_score = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=False, default=0)
    team2_score = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=False, default=0)
    team1_id = sqlalchemy.Column(UUID, sqlalchemy.ForeignKey("mfc_teams.id", ondelete="SET NULL"), nullable=True)
    team2_id = sqlalchemy.Column(UUID, sqlalchemy.ForeignKey("mfc_teams.id", ondelete="SET NULL"), nullable=True)
    sets = relationship(Set, cascade="all, delete")

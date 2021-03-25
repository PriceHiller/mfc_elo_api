import sqlalchemy

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase

from .round import Round


class Set(ModelBase, AlcBase):
    __tablename__ = "mfc_sets"

    team1_rounds_won = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=False, default=0)
    team2_rounds_won = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=False, default=0)
    match_id = sqlalchemy.Column(UUID, sqlalchemy.ForeignKey("mfc_matches.id"))
    rounds = relationship(Round, cascade="all, delete")

import sqlalchemy

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase

from .set import Set


class Match(ModelBase, AlcBase):
    """
    @Task, @Todo, [Complete Documentation]
        Example: A set is defined as the summation, first to 7, ...
    """

    __tablename__ = "mfc_matches"

    team1_sets_won = sqlalchemy.Column(sqlalchemy.Float, index=True, nullable=False, default=0)
    team2_sets_won = sqlalchemy.Column(sqlalchemy.Float, index=True, nullable=False, default=0)

    team1_id = sqlalchemy.Column(
        UUID,
        sqlalchemy.ForeignKey("mfc_teams.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    team2_id = sqlalchemy.Column(
        UUID,
        sqlalchemy.ForeignKey("mfc_teams.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    sets = relationship(Set, cascade="all, delete")

import sqlalchemy

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase

from .round import Round


class Set(ModelBase, AlcBase):
    __tablename__ = "mfc_sets"

    match_id = sqlalchemy.Column(UUID, sqlalchemy.ForeignKey("mfc_matches.id", ondelete="CASCADE"), index=True)
    rounds = relationship(Round, cascade="all, delete", passive_deletes=True)

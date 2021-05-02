import sqlalchemy

from sqlalchemy.dialects.postgresql import UUID

from API.Database.Models import ModelBase
from API.Database.Models import AlcBase


class Player(ModelBase, AlcBase):
    __tablename__ = "mfc_players"

    player_name = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False, unique=False)
    playfab_id = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True, nullable=False)
    discord_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, index=True, nullable=True)
    team_id = sqlalchemy.Column(
        UUID,
        sqlalchemy.ForeignKey("mfc_teams.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    ambassador = sqlalchemy.Column(
        sqlalchemy.Boolean,
        index=True
    )

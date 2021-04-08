import sqlalchemy

from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class DiscordID:
    discord_id = sqlalchemy.Column(
        sqlalchemy.String,
        index=True,
    )


@as_declarative()
class PermissionJSON:
    permission_col = sqlalchemy.Column(
        sqlalchemy.JSON,
        nullable=True
    )

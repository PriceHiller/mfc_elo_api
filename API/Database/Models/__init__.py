import uuid
import logging
import sqlalchemy

from datetime import datetime
from datetime import timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declarative_base
from API import find_subclasses

AlcBase = declarative_base()

metadata = MetaData()

log = logging.getLogger(__name__)


@as_declarative()
class ModelBase:
    """
    Credit for modification and creation attributes: Jacob Sanders, https://gitlab.cloud-technology.io/segmentational
    """

    __table__: sqlalchemy.Table
    id = sqlalchemy.Column(
        UUID,
        server_default=sqlalchemy.text("uuid_generate_v4()"),
        primary_key=True,
    )

    creation: sqlalchemy.Column = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        key="creation",
        name="creation",
        index=True,
        quote=True,
        unique=False,
        default=None,
        nullable=False,
        primary_key=False,
        autoincrement=False,
        server_default=sqlalchemy.func.now(),
    )

    modification: sqlalchemy.Column = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        key="Modification",
        name="modification",
        index=True,
        quote=True,
        unique=False,
        default=None,
        nullable=True,
        onupdate=sqlalchemy.func.now(),
        primary_key=False,
        autoincrement=False
    )

    @staticmethod
    def load_models():
        find_subclasses(__package__)
        for subclass in ModelBase.__subclasses__():
            log.info(f"Loaded model: \"{subclass.__name__}\" ({subclass.__module__})")

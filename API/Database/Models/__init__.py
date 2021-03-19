import uuid
import logging
import sqlalchemy
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
    __table__: sqlalchemy.Table

    primary_key = sqlalchemy.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=uuid.uuid4,
    )

    @staticmethod
    def load_models():
        find_subclasses(__package__)
        for subclass in ModelBase.__subclasses__():
            log.info(f"Loaded model: \"{subclass.__name__}\" ({subclass.__module__})")

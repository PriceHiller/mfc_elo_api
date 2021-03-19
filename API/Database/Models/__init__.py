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
    id = sqlalchemy.Column(UUID, server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True)

    @staticmethod
    def load_models():
        find_subclasses(__package__)
        for subclass in ModelBase.__subclasses__():
            log.info(f"Loaded model: \"{subclass.__name__}\" ({subclass.__module__})")

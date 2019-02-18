from sqlalchemy import Column, Integer, DateTime, String, Float, Text, Date
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy_utils.models import generic_repr

from connectors.db_connection import Base


@generic_repr
class WeatherStationsModel(Base):
    __tablename__ = "stations"

    station_id = Column(String, primary_key=True)
    from_date = Column(Date(), nullable=True)
    to_date = Column(Date(), nullable=True)
    stations_hoehe = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    station_name = Column(String)


@generic_repr
class CeleryTaskMetaModel(Base):
    __tablename__ = "celery_taskmeta"
    id = Column(Integer, autoincrement=True, primary_key=True)
    task_id = Column(String(155), nullable=True, unique=True)
    status = Column(String(50), nullable=True)
    result = Column(BYTEA(), nullable=True)
    date_done = Column(DateTime(), nullable=True)
    traceback = Column(Text(), nullable=True)


@generic_repr
class CeleryTaskSetMetaModel(Base):
    __tablename__ = "celery_tasksetmeta"

    id = Column(Integer, autoincrement=True, primary_key=True)
    taskset_id = Column(String(155), nullable=True, unique=True)
    result = Column(BYTEA(), nullable=True)
    date_done = Column(DateTime(), nullable=True)

from connectors.db_connection import get_db_session_scope
from handlers.utils.base_schema import BaseSchema
from models.postgres import WeatherStationsModel


class StationSchema(BaseSchema):
    class Meta:
        model = WeatherStationsModel


class DBStationsHandler:

    schema = StationSchema()
    model = WeatherStationsModel

    @classmethod
    def add(cls, **kwargs):
        validation = cls.schema.load(data=kwargs)
        if validation.errors:
            raise Exception(validation.errors)

        with get_db_session_scope() as session:
            session.add(validation.data)

    @classmethod
    def get_all(cls):
        """
        """
        with get_db_session_scope() as session:
            query = session.query(cls.model)
            return cls.schema.dump(query.all(), many=True).data

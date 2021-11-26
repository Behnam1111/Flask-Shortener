from sqlalchemy import Column, String, Integer, MetaData, create_engine, inspect, Table
from fus_url.config.runtime_config import RuntimeConfig
from fus_url.dao.base_dao import BaseDao
from fus_url.model.request_model import Request


class RequestDao(BaseDao):

    def __init__(self):
        super(RequestDao, self).__init__()
        self.model = Request

    @staticmethod
    def create_table():
        engine = create_engine(
            "mysql://{username}:{password}@{host}/{schema}".format(username=RuntimeConfig.DB_USERNAME,
                                                                   password=RuntimeConfig.DB_PASSWORD,
                                                                   host=RuntimeConfig.DB_HOST,
                                                                   schema=RuntimeConfig.DB_SCHEMA), echo=False)
        insp = inspect(engine)
        if not insp.has_table(engine, "requests"):
            metadata_obj = MetaData()
            Table("requests", metadata_obj,
                  Column('id', Integer, primary_key=True, nullable=False),
                  Column('ip_address', String(50)),
                  Column('mobile_desktop_type', String(50)),
                  Column('request_timestamp', Integer),
                  Column('elapsed_time', String(20)),
                  Column('short_url', String(50))
                  )
            metadata_obj.create_all(engine)

    def add(self, ip_address, mobile_desktop_type, request_timestamp, elapsed_time, short_url):
        request = Request(ip_address, mobile_desktop_type, request_timestamp, elapsed_time, short_url)
        self.session.add(request)
        self.session.commit()

    def get_all_requests(self):
        requests_db = self.session.query(self.model).all()
        return requests_db


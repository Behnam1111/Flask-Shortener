from sqlalchemy import Column, String, Integer, MetaData, create_engine, inspect, Table
from fus_url.config.runtime_config import RuntimeConfig
from fus_url.dao.base_dao import BaseDao
from fus_url.model.url_model import Url


class UrlDao(BaseDao):
    def __init__(self):
        super(UrlDao, self).__init__()
        self.model = Url

    @staticmethod
    def create_table():
        engine = create_engine("mysql://{username}:{password}@{host}/{schema}".format(username=RuntimeConfig.DB_USERNAME,
                                                                   password=RuntimeConfig.DB_PASSWORD,
                                                                   host=RuntimeConfig.DB_HOST,
                                                                   schema=RuntimeConfig.DB_SCHEMA), echo=False)
        insp = inspect(engine)
        if not insp.has_table(engine, "urls"):
            metadata_obj = MetaData()
            Table("urls", metadata_obj,
                  Column('id', Integer, primary_key=True, nullable=False),
                  Column('short_url', String(50)),
                  Column('original_url', String(500)),
                  Column('timestamp', Integer))

            metadata_obj.create_all(engine)

    def add(self, short_url, original_url, timestamp):
        url = Url(short_url, original_url, timestamp)
        self.session.add(url)
        self.session.commit()

    def get_url_by_short_url(self, short_url):
        original_url = self.session.query(self.model).filter(Url.short_url == short_url).first().original_url
        return original_url

    def get_last_url_id(self):
        last_url_record = self.session.query(self.model).order_by(self.model.id.desc()).first()
        if last_url_record:
            last_url_id = last_url_record.id
        else:
            last_url_id = 1
        return last_url_id


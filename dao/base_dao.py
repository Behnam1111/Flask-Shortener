import sqlalchemy as db

from sqlalchemy.orm import scoped_session, sessionmaker

from fus_url.config.runtime_config import RuntimeConfig


class BaseDao:
    def __init__(self):
        engine = db.create_engine(
            "mysql://{username}:{password}@{host}/{schema}".format(username=RuntimeConfig.DB_USERNAME,
                                                                   password=RuntimeConfig.DB_PASSWORD,
                                                                   host=RuntimeConfig.DB_HOST,
                                                                   schema=RuntimeConfig.DB_SCHEMA), echo=False)

        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=engine))
        self.conn = engine.connect()
        self.model = None

    def get_all(self):
        return self.session.query(self.model).all()

    def get_by_id(self, _id):
        return self.session.query(self.model).filter(self.model.id == _id).first()

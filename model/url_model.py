from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from fus_url.model.base_model import Base


class Url(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    short_url = Column(String)
    original_url = Column(String)
    timestamp = Column(Integer)

    def __init__(self, short_url, original_url, timestamp):
        self.short_url = short_url
        self.original_url = original_url
        self.timestamp = timestamp

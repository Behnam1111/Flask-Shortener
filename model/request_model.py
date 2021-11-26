from datetime import datetime

from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from fus_url.model.base_model import Base
from fus_url.model.url_model import Url


class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    mobile_desktop_type = Column(String)
    request_timestamp = Column(Integer)
    elapsed_time = Column(String)
    short_url = Column(String, ForeignKey(Url.short_url))
    url = relationship('Url', foreign_keys='Request.short_url')

    def __init__(self, ip_address, mobile_desktop_type, request_timestamp, elapsed_time, short_url):
        self.ip_address = ip_address
        self.mobile_desktop_type = mobile_desktop_type
        self.request_timestamp = request_timestamp
        self.elapsed_time = elapsed_time
        self.short_url = short_url


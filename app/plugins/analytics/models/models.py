# -*- coding: utf-8 -*-
from flask_marshmallow import Marshmallow
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
ma = Marshmallow()


class URL(Base):
    __tablename__ = 'urls'
    name = Column(String, primary_key=True, nullable=False)
    total_visits = Column(Integer, default=0)

    def __init__(self, name, total_visits=0):
        self.name = name
        self.total_visits = total_visits


class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    total_visits = Column(Integer, default=0)

    url_id = Column(Integer, ForeignKey('urls.name'))

    url = relationship('URL')

    def __init__(self, date, url_id, total_visits=0):
        self.date = date
        self.url_id = url_id
        self.total_visits = total_visits

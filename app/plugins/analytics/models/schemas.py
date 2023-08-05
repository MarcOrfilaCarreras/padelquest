# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields

from .models import Day
from .models import ma
from .models import URL

db = SQLAlchemy()


class URLSchema(ma.SQLAlchemySchema):
    class Meta:
        model = URL

    name = ma.auto_field()
    total_visits = ma.auto_field()


class DaySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Day

    total_visits = ma.auto_field()
    url = ma.auto_field()

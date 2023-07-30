# -*- coding: utf-8 -*-
class Production:
    # Flask
    DEBUG = False

    # SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://padelquest:padelquest@db:3306/padelquest'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    IMAGE_FOLDER = './images'
    CRON_MINUTES = 5


class Development:
    # Flask
    DEBUG = True

    # SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://padelquest:root@127.0.0.1:3306/padelquest'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    IMAGE_FOLDER = './images'
    CRON_MINUTES = 5

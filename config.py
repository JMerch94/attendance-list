from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    APP_NAME = environ['APP_NAME']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///attendance.db'


class DevConfig(Config):
    APP_NAME = environ['APP_NAME']
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///attendance-dev.db'

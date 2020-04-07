from os import environ


class Config:
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    FLAS_ENV = environ.get('FLASK_ENV')

    # DB
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

import os

class DefaultConfig(object):
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(DefaultConfig):
    DEBUG = False

class DevelopmentConfig(DefaultConfig):
    DEVELOPMENT = True
    DEBUG = True

import os
import json

with open('/etc/config.json') as config_file:
        config = json.load(config_file)
class DefaultConfig(object):
    DEBUG = False
    SECRET_KEY = config['SECRET_KEY']
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = config['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(DefaultConfig):
    DEBUG = False

class DevelopmentConfig(DefaultConfig):
    DEVELOPMENT = True
    DEBUG = True

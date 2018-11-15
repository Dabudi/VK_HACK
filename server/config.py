import os
basedir = os.path.dirname(__file__)

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tables.db'

import os

DEBUG = True
SECRET_KEY = os.urandom(24)

PROT = '3306'
HOST_NAME = '127.0.0.1'
DATABAES = 'equipment'
USERNAME = 'root'
PASSWORD = 'root666'

DB_URI = "mysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME , PASSWORD , HOST_NAME , PROT , DATABAES)

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

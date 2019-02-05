import datetime
from peewee import *
import logging

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

logger.info('The next 2 lines of code are the only database specific code')
# database = SqliteDatabase('Customer.db')
# db = SqliteDatabase(':memory:')
db = SqliteDatabase('my_tweet.db', pragmas={'foreign_keys': 1})
db.connect()
# database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = TextField()


class Tweet(BaseModel):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref='tweets')


class Favorite(BaseModel):
    user = ForeignKeyField(User, backref='favorites')
    tweet = ForeignKeyField(Tweet, backref='favorites')
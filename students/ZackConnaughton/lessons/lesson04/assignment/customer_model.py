"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""

import os
import logging
from peewee import CharField, SqliteDatabase, FloatField, Model, BooleanField
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#reassign the global if environment is test

DATABASE = SqliteDatabase(config.DATABASE)


def create_database():
    DATABASE.connect()
    DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

    DATABASE.create_tables([
        Customer
        ])
    DATABASE.close()

class BaseModel(Model):
    class Meta:
        database = DATABASE

class Customer(BaseModel):
    """
        This class defines Customers info.
    """
    customer_id = CharField(primary_key=True, max_length=40)
    name = CharField(max_length=40)
    last_name = CharField(max_length=40)
    home_address = CharField(max_length=40)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=40)
    status = BooleanField()
    credit_limit = FloatField()

    class Meta:
        database = DATABASE

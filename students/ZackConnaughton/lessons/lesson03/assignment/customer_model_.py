"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""

import os
from peewee import CharField, SqliteDatabase, FloatField, Model, BooleanField

def create_database(db):
    if not os.path.isfile(db):
        database = SqliteDatabase(db)
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        database.create_tables([
            Customer
            ])
        database.close()


class Customer(Model, db):
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
        database = SqliteDatabase(db)

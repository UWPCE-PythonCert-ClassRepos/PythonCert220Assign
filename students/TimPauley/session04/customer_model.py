#Tim Pauley
#Python 220, Assignment 04
#Jan 2s9 2019

#Assignment 04: 

import logging
import peewee
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# wierdness of peewee we have to have this in global space, but not a constant
database = peewee.SqliteDatabase(config.DATABASE)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """Model to hold customer information"""
    customer_id = peewee.CharField(primary_key=True, max_length=20)
    first_name = peewee.CharField(max_length=40)
    last_name = peewee.CharField(max_length=40)
    home_address = peewee.CharField(max_length=60)
    phone_number = peewee.CharField(max_length=12)
    email_address = peewee.CharField(max_length=30)
    status = peewee.BooleanField()  # needs to be active or inactive
    credit_limit = peewee.FloatField()


def create_cust_table():
    with database:
        database.create_tables([Customer])


def delete_cust_table():
    """
    delete the customer table
    """
    del_cust = Customer.delete()
    del_cust.execute()


if __name__ == "__main__":
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
    create_tables()

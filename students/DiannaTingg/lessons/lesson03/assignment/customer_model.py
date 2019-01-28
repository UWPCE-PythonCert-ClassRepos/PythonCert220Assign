"""
Define schema for customer model.
"""

import logging
from peewee import SqliteDatabase, Model, CharField, BooleanField, DecimalField

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Connecting to a sqlite database.')

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
    Defining data fields for a customer.
    """
    logger.info('Defining the Customer class.')
    customer_id = CharField(primary_key=True, max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=100)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=100)
    active_status = BooleanField()
    credit_limit = DecimalField(max_digits=7, decimal_places=2)

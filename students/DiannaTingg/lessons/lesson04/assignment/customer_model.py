"""
Define schema for the customer model.
"""

import logging
import peewee as pw
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Connecting to a sqlite database.")

database = pw.SqliteDatabase(config.DATABASE)
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(pw.Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
    Defining the data fields for a customer.
    """
    customer_id = pw.CharField(primary_key=True, max_length=10)
    first_name = pw.CharField(max_length=30)
    last_name = pw.CharField(max_length=30)
    home_address = pw.CharField(max_length=100)
    phone_number = pw.CharField(max_length=20)
    email_address = pw.CharField(max_length=50)
    status = pw.CharField(max_length=15)
    credit_limit = pw.DecimalField(max_digits=10, decimal_places=2)

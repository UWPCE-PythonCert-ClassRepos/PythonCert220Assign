import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """Model to hold customer information"""
    customer_id = CharField(primary_key=True, max_length=20)
    first_name = CharField(max_length=40)
    last_name = CharField(max_length=40)
    home_address = CharField(max_length=60)
    phone_number = CharField(max_length=12)
    email_address = CharField(max_length=30)
    status = BooleanField()  # needs to be active or inactive
    credit_limit = FloatField()

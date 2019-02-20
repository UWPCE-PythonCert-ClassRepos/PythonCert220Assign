"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""
import logging
from peewee import Model, CharField, DecimalField, BooleanField, SqliteDatabase, DoesNotExist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Customers(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info('Must be a unique identifier for each person')
    customer_id = CharField(primary_key=True, max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=40)
    home_address = CharField(max_length=100)
    phone_number = CharField(max_length=30)
    email_address = CharField(max_length=100)
    status = BooleanField(default=False)
    credit_limit = DecimalField(max_digits=7, decimal_places=2)

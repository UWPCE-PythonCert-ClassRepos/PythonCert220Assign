"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""
import logging
from peewee import Model, CharField, BooleanField, FloatField, SqliteDatabase

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Here we define our data (the schema)')
LOGGER.info('First name and connect to a database (sqlite here)')

LOGGER.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only

LOGGER.info('This means we can easily switch to a different database')

LOGGER.info('Enable the Peewee magic! This base class does it all')


class BaseModel(Model):
    class Meta:
        database = database

LOGGER.info('By inheritance only we keep our model (almost) technology neutral')


class Customer(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    LOGGER.info('Note how we defined the class')

    LOGGER.info('Specify the fields in our model, their lengths and if mandatory')
    LOGGER.info('Must be a unique identifier for each person')
    customer_id = CharField(primary_key=True, max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=100)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=100)
    status = BooleanField()
    credit_limit = FloatField()

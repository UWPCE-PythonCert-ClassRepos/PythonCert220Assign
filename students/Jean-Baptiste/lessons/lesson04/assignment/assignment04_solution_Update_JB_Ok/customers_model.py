"""
    In this model we will create a simple database example with Peewee ORM, sqlite and Python
    then we will define the schema using logging
"""
from peewee import Model, CharField, BooleanField, FloatField, SqliteDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Here we will define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')
logger.info('The next 3 lines of code are the only database specific code')
database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')
logger.info('This means we can easily switch to a different database')
logger.info('Enable the Peewee magic! This base class does it all')

"""
This class defines Person, which maintains details of someone
for whom we want to research career to date.
This is to define our model using class
"""

class BaseModel(Model):
    class Meta:
        database = database
        logger.info('By inheritance only we keep our model (almost) technology neutral')

class Customer(BaseModel):
    logger.info('Note how we defined the class')
    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique identifier for each person')
    id = CharField(primary_key=True, max_length=30)
    first_name = CharField(max_length=40)
    last_name = CharField(max_length=40)
    home_address = CharField(max_length=120)
    phone_number = CharField(max_length=30)
    email_address = CharField(max_length=120)
    status = BooleanField()
    credit_limit = FloatField()


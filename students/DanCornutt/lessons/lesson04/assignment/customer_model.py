"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema

"""
import logging
from peewee import Model, CharField, BooleanField, FloatField, SqliteDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
        This class defines Customer, which maintains details of customers
        for whom we want to research career to date.
    """
    logger.info('Note how we defined the class')

    logger.info('Specify the fields in our model, their lengths and if \
    mandatory')
    logger.info('Must be a unique identifier for each customer')

    customer_id = CharField(primary_key=True, max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=50)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=20)
    status = BooleanField()
    credit_limit = FloatField()

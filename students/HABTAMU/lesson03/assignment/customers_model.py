"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from peewee import Model, MetaField, CharField, BooleanField, FloatField, SqliteDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we create a customer model and database that can be used at HP Norton')
logger.info('First connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')
database = SqliteDatabase('Customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
        This class defines Customer, help us to store customer data from HP Norton in a relational database (sqlite3),
        which maintains details of Customer for whom we want to research purchase and rental service.
    """
    
    customer_id = CharField(primary_key=True, max_length=30)
    first_name = CharField(max_length = 30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length= 100)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=100)
    status = BooleanField()
    credit_limit = FloatField()

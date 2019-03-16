"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

logging.info('Here we define our data (the schema)')
logging.info('First name and connect to a database (sqlite here)')

logging.info('The next 3 lines of code are the only database specific code')

db = SqliteDatabase('customer.db')
db.connect()
db.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


logging.info('This means we can easily switch to a different database')

logging.info('Enable the Peewee magic! This base class does it all')

class BaseModel(Model):
    class Meta:
        database = db

logging.info('By inheritance only we keep our model (almost) technology neutral')

class Customer(BaseModel):
    """
        This class defines Customer, which maintains customer details.
    """

    logging.info('Specify the fields in our model, their lengths and if mandatory')
    logging.info('Must be a unique identifier for each person')
    id = PrimaryKeyField(primary_key = True)
    first_name = CharField(max_length = 30)
    last_name = CharField(max_length = 30)
    home_address = CharField(max_length = 30)
    phone_number = CharField(max_length = 30)
    email_address = CharField(max_length = 30)
    status = BooleanField()
    credit_limit = DecimalField(max_digits = 9, decimal_places = 2)

class Furniture(BaseModel):
    """
        This class defines Furniture, which maintains furniture details. I
        made this just so I could see another table in the db :)
    """
    logging.info('The Furniture table is not going to be used')
    id = IntegerField(primary_key = True)
    furniture_name =  CharField(max_length = 30)

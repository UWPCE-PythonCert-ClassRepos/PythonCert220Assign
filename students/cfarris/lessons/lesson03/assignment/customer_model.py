#!/usr/bin/env Python3

"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

# if you wanted to use heroku postgres:
#
# psycopg2
#
# parse.uses_netloc.append("postgres")
# url = parse.urlparse(os.environ["DATABASE_URL"])
#
# conn = psycopg2.connect(
# database=url.path[1:],
# user=url.username,
# password=url.password,
# host=url.hostname,
# port=url.port
# )
# database = conn.cursor()
#
# Also consider elephantsql.com (be sure to use configparser for PWß)

logger.info('This means we can easily switch to a different database')

logger.info('Enable the Peewee magic! This base class does it all')

class BaseModel(Model):
    class Meta:
        database = database

#logger.info('By inheritance only we keep our model (almost) technology neutral')


class Customer(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want store their data.
    """
    logger.info('Note how we defined the class')
    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique identifier for each person')

    customer_id = CharField(primary_key = True, max_length=15)
    first_name = CharField(max_length = 30)
    last_name = CharField(max_length = 30)
    home_address = CharField(max_length = 100)
    nickname = CharField(max_length = 20, null = True)
    home_address=CharField(max_length=100) #started here
    phone_number = CharField(max_length=20)
    email_address= CharField(max_length=100)
    status = BooleanField()
    credit_limit = FloatField()

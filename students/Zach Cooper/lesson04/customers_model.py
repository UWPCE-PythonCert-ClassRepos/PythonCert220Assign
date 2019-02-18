"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""
import logging
import config
import peewee as pw


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('First name and connect to a database (sqlite here)')

LOGGER.info('The next 3 lines of code are the only database specific code')

DATABASE = pw.SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only

LOGGER.info('This means we can easily switch to a different database')

LOGGER.info('Enable the Peewee magic! This base class does it all')


class BaseModel(pw.Model):
    """
        Creating BaseModel class
    """
    class Meta:
        database = DATABASE

LOGGER.info('By inheritance only we keep our model (almost) technology neutral')


class Customer(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    LOGGER.info('Note how we defined the class')

    LOGGER.info('Specify the fields in our model, their lengths and if mandatory')
    LOGGER.info('Must be a unique identifier for each person')
    customer_id = pw.CharField(primary_key=True, max_length=30)
    first_name = pw.CharField(max_length=30)
    last_name = pw.CharField(max_length=30)
    home_address = pw.CharField(max_length=100)
    phone_number = pw.CharField(max_length=20)
    email_address = pw.CharField(max_length=50)
    status = pw.CharField(max_length=15)
    credit_limit = pw.DecimalField(max_digits=10, decimal_places=2)


"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only

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


class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
        This creates a customer model
    """
    customer_id = CharField(primary_key=True, max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=40)
    home_address = CharField(max_length=100)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=100)
    status = BooleanField()
    credit_limit = FloatField()

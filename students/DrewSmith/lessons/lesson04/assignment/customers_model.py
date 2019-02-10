"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""


import logging
import peewee as pw
import assignment.create_customers as cc

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class BaseModel(pw.Model):
    ''' Base class for all database models '''
    class Meta:
        ''' BaseModel Meta class '''
        database = cc.get_database()

class Customer(BaseModel):
    """
    This class defines Customer, which maintains customer details
    """
    customer_id = pw.CharField(primary_key=True, max_length=30)
    first_name = pw.CharField(max_length=30)
    last_name = pw.CharField(max_length=30)
    home_address = pw.CharField(max_length=100)
    phone_number = pw.CharField(max_length=20)
    email_address = pw.CharField(max_length=100)
    status = pw.BooleanField()
    credit_limit = pw.FloatField()

"""
This is to create database using the Peewee ORM, sqlite and Python

"""
from  customers_model import *
import customers_model as cm
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Let us build the classes from the model in the database')
cm.database.create_tables([cm.Customer])
cm.database.close()

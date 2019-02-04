#Tim Pauley
#Assignment 03
#Jan 22 2019


""" 
    Create database examle with Peewee ORM, sqlite and Python

"""

import customers_model as cm
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

logger.info('Here we dinew our data schema')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database.create_tables([
        Job,
        Person,
        PersonNumKey
    ])

database.close()

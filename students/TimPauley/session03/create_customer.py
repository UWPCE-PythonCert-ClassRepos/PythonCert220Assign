#Tim Pauley
#Assignment 03
#Jan 22 2019


""" 
    Create database examle with Peewee ORM, sqlite and Python

"""

import customers_model as cm

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

database.create_tables([
        Job,
        Person,
        PersonNumKey
    ])

database.close()

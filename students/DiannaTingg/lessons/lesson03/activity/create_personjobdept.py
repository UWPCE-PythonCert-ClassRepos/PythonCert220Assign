"""
    Create database example with Peewee ORM, sqlite and Python
"""

from personjobdept_model import *

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

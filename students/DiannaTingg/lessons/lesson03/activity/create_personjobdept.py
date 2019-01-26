"""
Create database example with Peewee ORM, sqlite and Python.
"""

import personjobdept_model as pjd

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

pjd.database.create_tables([
        pjd.Department,
        pjd.Job,
        pjd.Person,
        pjd.PersonNumKey
    ])

pjd.database.close()

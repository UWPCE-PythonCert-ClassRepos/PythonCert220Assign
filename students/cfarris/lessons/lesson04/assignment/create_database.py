#!/usr/bin/env Python3
"""
    Create database examle with Peewee ORM, sqlite and Python

"""
import logging
import customer_model as cm



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')


def create_tables():
    cm.database.create_tables([cm.Customer])
    cm.database.close()
    return cm.database




create_tables()

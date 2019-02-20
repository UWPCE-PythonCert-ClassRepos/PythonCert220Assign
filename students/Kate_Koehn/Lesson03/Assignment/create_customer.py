"""
    Create database example with Peewee ORM, SQLite and Python

"""

import customer_model as cm

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')



def create_tables():
    cm.database.create_tables([
            cm.Customers
        ])
    cm.database.close()
    return cm.database


if __name__ == "__main__":
    database = create_tables()


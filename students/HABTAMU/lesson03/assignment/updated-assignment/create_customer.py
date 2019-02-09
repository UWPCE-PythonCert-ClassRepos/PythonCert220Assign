"""
    Create database example with Peewee ORM, SQLite and Python
"""

import customers_model as cm
import logging


def main():
    """
    :return:   Create database
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('One off program to build the classes from the model in the database')

    cm.database.create_tables([cm.Customer])

    cm.database.close()
    # return cm.database

"""
Create a customers database for Norton Furniture using peewee, sqlite, and Python.
"""

import logging
import customer_model as cm


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Creating a database using the customer model.")

    cm.database.create_tables([cm.Customer])

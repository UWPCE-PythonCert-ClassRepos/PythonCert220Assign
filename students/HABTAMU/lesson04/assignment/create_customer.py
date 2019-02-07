"""
    Create database example with Peewee ORM, SQLite and Python
"""

import customers_model as cm
import logging

# Create a custom logger
logger = logging.getLogger(__name__ + '.create_customer')
logger.setLevel(logging.DEBUG)

# Create handlers
f_handler = logging.FileHandler('db.log')

# Create formatter and add it to handlers
f_format = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s')
f_handler.setLevel(logging.INFO)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(f_handler)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(f_format)

def main():
    """
    :return:   Create database
    """
    logger.info('One off program to build the classes from the model in the database')
    cm.database.create_tables([cm.Customer])
    cm.database.close()

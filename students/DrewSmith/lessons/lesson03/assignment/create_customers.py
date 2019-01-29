"""
    Manage database environment with Peewee ORM, sqlite and Python
"""

import logging
import sqlite3
from sqlite3 import Error
import peewee as pw


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DATABASE = None

def model_setup(environment="prod"):
    '''
    Enables and sets up the Database for customers

    :param environment: prod to use customers.db
        or 'test' to use customers_test.db
    '''

    global DATABASE
    connect = "customers.db"
    if environment == "test":
        connect = "customers_test.db"

    if DATABASE is None:
        try:
            conn = sqlite3.connect(connect)
        except Error as error:
            LOGGER.error(error)
        else:
            LOGGER.info(f"{connect} database active")
        finally:
            conn.close()

        DATABASE = pw.SqliteDatabase(connect)
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
        LOGGER.info("Database setup")

    return DATABASE

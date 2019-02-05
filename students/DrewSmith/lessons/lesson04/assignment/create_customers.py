"""
    Manage database environment with Peewee ORM, sqlite and Python
"""

import logging
import sqlite3
from sqlite3 import Error
import peewee as pw


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

connection = "customers.db"

def get_database(env="prod"):
    '''
    Enables and sets up the Database for customers

    :param env: prod to use customers.db
        or 'test' to use customers_test.db
    '''

    global connection
    if env == "test":
        connection = "customers_test.db"

    try:
        conn = sqlite3.connect(connection)
    except Error as error:
        LOGGER.error(error)
    else:
        LOGGER.info(f"{connection} database active")
    finally:
        conn.close()

    database = pw.SqliteDatabase(connection)
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    return database

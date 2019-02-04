"""
    Create database examle with Peewee ORM, sqlite and Python

"""

import logging
import peewee as pw

global db


def setup_db():
    logging.basicConfig(level=logging.INFO)
    LOGGER = logging.getLogger(__name__)

    LOGGER.info('One off program to build the classes from the model in the database')

    db = pw.SqliteDatabase('personjobxxx.db')
    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

    return db
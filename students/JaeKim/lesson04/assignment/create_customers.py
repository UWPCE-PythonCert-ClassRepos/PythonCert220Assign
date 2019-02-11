"""
    Create database examle with Peewee ORM, sqlite and Python

"""

import logging
import peewee as pw

db = None

def setup_db(environment='prod'):
    global db
    logging.basicConfig(level=logging.INFO)
    LOGGER = logging.getLogger(__name__)

    LOGGER.info('One off program to build the classes from the model in the database')
    if environment == 'prod':
        db = pw.SqliteDatabase('personjob.db')
        print('prod')

    elif environment == 'dev':
        db = pw.SqliteDatabase('personjob-dev.db')
        print('dev')


    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

    return db
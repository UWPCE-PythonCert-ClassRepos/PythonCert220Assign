"""
    Create database examle with Peewee ORM, sqlite and Python

"""
import logging
import os
from customer_model import Customer as cm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not os.path.isfile('customer.db'):
    cm.database.connect()
    cm.database.execute_sql('PRAGMA foreign_keys = ON;')

    cm.database.create_tables([
        cm.Customer
    ])

    cm.database.close()

"""
    Create database examle with Peewee ORM, sqlite and Python

"""

from customer_model import *

import logging
import sqlite3
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

# database.create_tables([
#         Customer,
#     ])
#
# database.close()

df = pd.read_csv('customer.csv', encoding='ISO-8859-1')

# using comprehension
df.columns = [x.lower() for x in df.columns]
df = df.rename(columns = {"id": "customer_id"})
df.to_sql('Customer', database)
database.close()


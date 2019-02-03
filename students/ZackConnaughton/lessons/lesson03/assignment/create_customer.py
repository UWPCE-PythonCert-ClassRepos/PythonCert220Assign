"""
    Create database examle with Peewee ORM, sqlite and Python

"""
import logging
import customer_model as cm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cm.database.create_tables([
        cm.Customer
    ])

cm.database.close()

"""
#Lesson03
#Customer Database Exercise ##
Create database examle with Peewee ORM, sqlite and Python
"""

#!/usr/bin/env python3
#import stuff here
import datetime
import logging
from peewee import *
from db_model import *

#global variables here

logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

logging.info('One off program to build the classes from the model in the database')

db.create_tables([
        Customer,
        Furniture
    ])

db.close()

#for testing
if __name__=="__main__":
    pass

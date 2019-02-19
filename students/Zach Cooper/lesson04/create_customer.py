"""
    Create database examle with Peewee ORM, sqlite and Python
"""

import customers_model as cm
import logging


def main():
    """
    Customer table created
    :return:
    """


    logging.basicConfig(level=logging.INFO)
    LOGGER = logging.getLogger(__name__)

    LOGGER.info("Customer database created using customer model")

    cm.DATABASE.create_tables([cm.Customer])


# def create_tables():
#     cm.database.create_tables([cm.Customer])
#     cm.database.close()
#     return cm.database

# data_file = pd.read_csv("customer.csv", encoding="ISO-8859-1")


# data_file.columns = [x.lower() for x in data_file.columns]
# data_file = data_file.rename(columns = {"id": "customer_id"})
# data_file.to_sql('Customer', database)
# database.close()


"""
    This creates a test.db seperate from the customer database
"""
# import logging
# import sqlite3
# from sqlite3 import Error
# import peewee as pw


# logging.basicConfig(level=logging.INFO)
# LOGGER = logging.getLogger(__name__)

# DATABASE = None

# def model_setup(environment="prod"):
#     '''
#     Enables and sets up the Database for customers
#     :param environment: prod to use customers.db
#         or 'test' to use customers_test.db
#     '''

#     global DATABASE
#     connect = "customers.db"
#     if environment == "test":
#         connect = "customers_test.db"

#     if DATABASE is None:
#         try:
#             conn = sqlite3.connect(connect)
#         except Error as error:
#             LOGGER.error(error)
#         else:
#             LOGGER.info(f"{connect} database active")
#         finally:
#             conn.close()

#         DATABASE = pw.SqliteDatabase(connect)
#         DATABASE.connect()
#         DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
#         LOGGER.info("Database setup")

#     return DATABASE

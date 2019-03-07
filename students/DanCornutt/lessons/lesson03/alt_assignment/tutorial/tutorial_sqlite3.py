import sqlite3

from sqlite3 import Error


def sql_connection():

    try:
        con = sqlite3.connect('mydatabase.db')
        print("Connection is established: Database is created in memory")
    except Error:
        print(Error)


def sql_table(con):
    """Creates db table and db"""
    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE customer(customer_id integer PRIMARY KEY, first_name text, last_name text, home_address text, phone_number text, email_address text, status boolean, credit_limit float)")
    con.commit()


def search_customer(con, customer_id):
    cursorObj = con.cursor()
    searched = cursorObj.execute("SELECT * FROM customer")
    return searched


if __name__ == __main__():
    con = sql_connection()
    sql_table(con)

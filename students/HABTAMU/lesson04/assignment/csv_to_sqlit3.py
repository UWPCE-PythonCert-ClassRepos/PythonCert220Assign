import sqlite3
import csv
import create_customer
import customers_model
import logging
from peewee import Model, CharField, BooleanField, FloatField, SqliteDatabase

f = open('lesson04_assignment_data_customer.csv', 'r', encoding="ISO-8859-1")  # open the csv data file
next(f, None)  # skip the header row
reader = csv.reader(f)

sql = sqlite3.connect('Customer.db')
cur = sql.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Customer
            (customer_id,
            first_name,
            last_name,
            home_address,
            phone_number,
            email_address,
            status,
            credit_limit)''')  # create the table if it doesn't already exist

for row in reader:
    cur.execute("INSERT INTO Customer VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row)

f.close()
sql.commit()
sql.close()

from pymongo import MongoClient
import csv
import database as d_base
import pytest
import pprint

client = MongoClient('localhost', '27017')
client.drop_database('HP_Norton')


def drop_db():
    client = MongoClient('localhost', '27017')
    client.drop_database('HP_Norton')

def create_db():
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient.HP_Norton

def create_collections():
    create_db()
    # Customers collection
    customers = db["customers"]
    # Products collection
    products = db["products"]
    # Rentals collection
    rentals = db["rentals"]

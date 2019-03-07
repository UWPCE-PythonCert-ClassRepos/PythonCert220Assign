from pymongo import MongoClient
#pprint library is used to make the output look more prerry
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('127.0.0.1')
# host='127.0.0.1', port=27017
db=client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)

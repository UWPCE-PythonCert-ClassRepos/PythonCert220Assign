#Tim Pauley
#Python 201a, HW 3
#Date: Jan 20 2019

import logging
from customers import

def populate_db():
	'''
	add customer data to database
	'''
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)

	database = SqliteDatabase('databaseNAME')

	logger.info('Working with customer class')
	logger.info('Note how I use constants and a list of tuples as a simple schema')
	logger.info('Normally you probably will have a pompted the user')

'''
Enter Table Schema here
'''

'''
Enter Table Data here
'''

	logger.info('Creating customer records: iterate through the list of tuples')
	logger.info('Prepare to explain any errors with exceptions')
	logger.info('and the transactions tells the database to fail an error')

	try:
		database.connect()
		database.execute_sql('PRAGMA foreign_keys = ON;')
		for customer in customer:
			with database.transactions():
				new_customer = Customer.create( 
					customer_name = customer[customer_name]
					, address = customer[address])
				new_customer.save()
				logger.info('Database add successfully')

		logger.info('Print the person records we saved....')
		for saved_customer in Customer:
			logger.info(f'{saved_customer} lives in {saved_customer.address} ' *\
				f' and likes to be known as {saved_customer.nickname}')

	except Exception as e:
		logger.info(f'Error creating = {customer[customer_name]}')
		logger.info(e)
		logger.info('see how the database protects are data')

	finally:
		logger.info('database closes')
		database.close()

if __name__ == '__main__':

'''
Stop video 5:40
'''			


#Tim Pauley
#Assignment 03
#Jan 22 2019

from basic_operations import add_customer
from customers_model import Customer


#create a dictionary here

def test_add_ok_customer():
	customer_id = 'W3434'
	name = 'Tim'
	last_name = 'Pauley'
	home_address = '1234 Queen Anne Ave N Seattle, Wa 98019'
	phone_number = '206-123-4567'
	email_address = 'too_can@gmail.com'
	status = True
	credit_limit = '40,0000'
	add_customer(
		customer_id
		,name
		,last_name
		,home_address
		,phone_number
		,email_address
		,status
		,credit_limit
		)	
		Customer.get(Customer.customer_id=customer_id)
		assert(test_customer.email_address = email_address)

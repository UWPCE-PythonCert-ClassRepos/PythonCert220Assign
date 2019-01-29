#Tim Pauley
#Assignment 03
#Jan 22 2018

"""
This file will need to have the following functions:

add_customer
(customer_id
	, name
	, lastname
	, home_address
	, phone_number
	, email_address
	, status
	, credit_limit): 

This function will add a new customer to the sqlite3 database.
search_customer(customer_id): This function will return a dictionary object with name, lastname, email address and phone number of a customer or an empty dictionary object if no customer was found.
delete_customer(customer_id): This function will delete a customer from the sqlite3 database.
update_customer_credit(customer_id, credit_limit): This function will search an existing customer by customer_id and update their credit limit or raise a ValueError exception if the customer does not exist.
list_active_customers(): This function will return an integer with the number of customers whose status is currently active.
Note: You can have other functions and code as required, but the five functions outlined above should be present and using the same amount of parameters. This is important, as those functions are how your code gets integrated into other sections of the project (such as the Web frontend).
Create some functional and unit tests for the model. Store them in the tests directory.
Develop functionality to deliver the requirements listed above.
Develop tests, and show some tests passing. Show other tests failing.
Ensure you application will create an empty database if one doesn’t exist when the app is first run. Call it customers.db
"""

	logger_info("")
	logger_info("") 
	customer_id = Charfield(primary)
	name = Charfield(max_length = 100)
	lastname = Charfield(max_length = 100)
	home_address = Charfield(max_length = 100)
	phone_number = Charfield(max_length = 100)
	email_address = Charfield(max_length = 100)
	status = BooleonField()
	credit_limit = FloatField()


"""
Test Configuration for Customer Model
"""
# I would normally do this in yaml or json, but did here for simplicity

# prod
# DATABASE = 'customers.db'

##### CHANGE DATABASE VARIABLE, NOT TEST_DATABASE

TEST_DATABASE = 'test.db'
DATABASE = TEST_DATABASE

### Should be in every config (normally would be separate config)
etext = {
    "not_found": "The customer with id: {} was not found",
    "req_bool": "Status was {}, must be 'Active', 'Inactive', True or False",
    "no_save": "We were unable to save customer with id {}, a required field was missing."
}

# Testing stuff
customer1 = {
    "customer_id": "0000001",
    "name": "Mickey",
    "last_name": "Mouse",
    "home_address": "DisneyLand",
    "phone_number": "123-456-7890",
    "email_address": "mickey@disney.com",
    "status": True,
    "credit_limit": 1000
    }

customer2 = {
    "customer_id": "0000002",
    "name": "Donald",
    "last_name": "Duck",
    "home_address": "DisneyLand",
    "phone_number": "987-654-3210",
    "email_address": "donald@disney.com",
    "status": True,
    "credit_limit": 10
    }

bad_customer = {
    "customer_id": "0000245",
    "name": "Madame",
    "last_name": "Medusa",
    "home_address": "DisneyLand",
    "phone_number": "666-666-6666",
    "email_address": "medusa@disney.com",
    "status": "hello",
    "credit_limit": 10
    }

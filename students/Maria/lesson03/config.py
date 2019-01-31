"""
Test Configuration for Customer Model
"""

TEST_DATABASE = 'test.db'
DATABASE = TEST_DATABASE


customer1 = {
    "customer_id": "0000001",
    "first_name": "Mickey",
    "last_name": "Mouse",
    "home_address": "DisneyLand",
    "phone_number": "123-456-7890",
    "email_address": "mickey@disney.com",
    "status": True,
    "credit_limit": 1000
    }

customer2 = {
    "customer_id": "0000002",
    "first_name": "Donald",
    "last_name": "Duck",
    "home_address": "DisneyLand",
    "phone_number": "987-654-3210",
    "email_address": "donald@disney.com",
    "status": True,
    "credit_limit": 10
    }

# prod
# database = 'customers.db'

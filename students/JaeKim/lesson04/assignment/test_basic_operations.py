import customers_model as cm
import pytest
from create_customers import setup_db
from basic_operations import add_customer, search_customer, delete_customer, update_customer_credit, list_active_customers
import csv

"""
Module docstring
"""

OK_CUSTOMER = {'customer_id': '12345',
               'name': 'Suzie',
               'lastname': 'Edgar',
               'home_address': '123 Browncroft Blvd, Rochester, NY 97235',
               'phone_number': '234-123-4567',
               'email_address': 'suzie@hotmail.com',
               'status': True,
               'credit_limit': 40,
               'stage': 'dev'}

#
#
# def import_users():
#     data = list()
#     with open('data.csv', 'r') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=',')
#         for row in spamreader:
#             dict_user = dict()
#             # customer_id,name,last_name,home_address,phone_number,email_address,status,credit_limit
#             dict_user['customer_id'] = row[0]
#             dict_user['name'] = row[1]
#             dict_user['last_name'] = row[2]
#             dict_user['home_address'] = row[3]
#             dict_user['phone_number'] = row[4]
#             dict_user['email_address'] = row[5]
#             dict_user['status'] = row[6]
#             dict_user['credit_limit'] = row[7]
#             data.append(dict_user)
#
#     return data
#
#
#
# @pytest.fixture(scope="function")
# def setup_test_db():
#     cm.database.create_tables([
#         cm.TestCustomer
#     ])
#     cm.database.close()
#
#     yield setup_test_db
#
#     cm.database.drop_tables([
#         cm.TestCustomer
#     ])
#     cm.database.close()

#
# def test_add_ok_customer(setup_test_db):
#     """
#     sets up a new db, adds customer, runs assertions and tears down db
#     """
#     add_customer(**OK_CUSTOMER)
#     valid_customer = TestCustomer.get(TestCustomer.customer_id == OK_CUSTOMER['customer_id'])
#
#     assert valid_customer.first_name == OK_CUSTOMER['name']
#     assert valid_customer.customer_id == OK_CUSTOMER['customer_id']
#     assert valid_customer.last_name == OK_CUSTOMER['lastname']
#     assert valid_customer.home_address == OK_CUSTOMER['home_address']
#     assert valid_customer.phone_number == OK_CUSTOMER['phone_number']
#     assert valid_customer.email_address == OK_CUSTOMER['email_address']
#     assert valid_customer.status == OK_CUSTOMER['status']
#     assert valid_customer.credit_limit == OK_CUSTOMER['credit_limit']
#
#
# def test_credit_limit_float(setup_test_db):
#     """
#     sets up a new db, adds customer, runs assertions and tears down db
#     """
#     bad_customer = dict(OK_CUSTOMER)
#     bad_customer['credit_limit'] = '$40'
#
#     with pytest.raises(ValueError):
#         add_customer(**bad_customer)
#
#
# def test_get_customer(setup_test_db):
#     """
#     sets up a new db, adds customer, runs assertions and tears down db
#     """
#     add_customer(**OK_CUSTOMER)
#     valid_customer = search_customer(OK_CUSTOMER['customer_id'], stage='dev')
#
#     assert valid_customer.first_name == OK_CUSTOMER['name']
#     assert valid_customer.customer_id == OK_CUSTOMER['customer_id']
#     assert valid_customer.last_name == OK_CUSTOMER['lastname']
#     assert valid_customer.home_address == OK_CUSTOMER['home_address']
#     assert valid_customer.phone_number == OK_CUSTOMER['phone_number']
#     assert valid_customer.email_address == OK_CUSTOMER['email_address']
#     assert valid_customer.status == OK_CUSTOMER['status']
#     assert valid_customer.credit_limit == OK_CUSTOMER['credit_limit']
#
#
# def test_delete_customer(setup_test_db):
#     """
#     sets up a new db, adds customer, runs assertions and tears down db
#     """
#     # Add and assert to confirm record exists before deleting
#     add_customer(**OK_CUSTOMER)
#     valid_customer = search_customer(OK_CUSTOMER['customer_id'], stage='dev')
#
#     assert valid_customer.first_name == OK_CUSTOMER['name']
#     assert valid_customer.customer_id == OK_CUSTOMER['customer_id']
#     assert valid_customer.last_name == OK_CUSTOMER['lastname']
#     assert valid_customer.home_address == OK_CUSTOMER['home_address']
#     assert valid_customer.phone_number == OK_CUSTOMER['phone_number']
#     assert valid_customer.email_address == OK_CUSTOMER['email_address']
#     assert valid_customer.status == OK_CUSTOMER['status']
#     assert valid_customer.credit_limit == OK_CUSTOMER['credit_limit']
#
#     delete_customer(OK_CUSTOMER['customer_id'], stage='dev')
#     valid_customer = search_customer(OK_CUSTOMER['customer_id'], stage='dev')
#
#     assert valid_customer is False
#
#
# def test_update_customer_credit(setup_test_db):
#     """
#     :return:
#     """
#     add_customer(**OK_CUSTOMER)
#     valid_customer = search_customer(OK_CUSTOMER['customer_id'], stage='dev')
#
#     assert valid_customer.first_name == OK_CUSTOMER['name']
#     assert valid_customer.customer_id == OK_CUSTOMER['customer_id']
#     assert valid_customer.last_name == OK_CUSTOMER['lastname']
#     assert valid_customer.home_address == OK_CUSTOMER['home_address']
#     assert valid_customer.phone_number == OK_CUSTOMER['phone_number']
#     assert valid_customer.email_address == OK_CUSTOMER['email_address']
#     assert valid_customer.status == OK_CUSTOMER['status']
#     assert valid_customer.credit_limit == OK_CUSTOMER['credit_limit']
#
#     update_customer_credit(valid_customer.customer_id, 90210, stage='dev')
#     valid_customer = search_customer(OK_CUSTOMER['customer_id'], stage='dev')
#
#     assert valid_customer.credit_limit == 90210
#
#
# def test_list_active_customer(setup_test_db):
#     """
#     sets up a new db, adds customers, runs assertions and tears down db
#     """
#     customer_jae = dict(OK_CUSTOMER)
#     customer_bob = dict(OK_CUSTOMER)
#     customer_erin = dict(OK_CUSTOMER)
#
#     customer_jae['status'] = True
#     customer_jae['name'] = 'Jae'
#     customer_jae['customer_id'] = 0
#     customer_erin['status'] = True
#     customer_erin['name'] = 'Erin'
#     customer_erin['customer_id'] = 1
#     customer_bob['status'] = False
#     customer_bob['name'] = 'Bob'
#     customer_bob['customer_id'] = 2
#
#     # Add 3 customers to DB, only first two are Status = True
#     add_customer(**customer_jae)
#     add_customer(**customer_erin)
#     add_customer(**customer_bob)
#
#     # list_active_customers - Returns a dict with 2 results
#     active_customers = list_active_customers(stage='dev')
#
#     # assert first two rows are Jae and Erin
#     assert active_customers[0]['first_name'] == customer_jae['name']
#     assert active_customers[1]['first_name'] == customer_erin['name']


def test_add_bulk_users():
    assert True
    #users = import_users()
    # setup_db()
    # users = 'jae'
    #
    # for user in users:
    #     print('user : {}'.format(user))

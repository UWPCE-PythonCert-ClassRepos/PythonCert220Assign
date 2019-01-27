import customers_model as cm
from customers_model import Test_Customer
from basic_operations import add_customer, search_customer, delete_customer, update_customer_credit, list_active_customers
import pytest

ok_customer = {'customer_id': '12345',
               'name': 'Suzie',
               'lastname': 'Edgar',
               'home_address': '123 Browncroft Blvd, Rochester, NY 97235',
               'phone_number': '234-123-4567',
               'email_address': 'suzie@hotmail.com',
               'status': True,
               'credit_limit': 40,
               'stage': 'dev'}


def setup_test_db():
    """
    Drops test_customer and re-creates an empty test_customer db
    """
    # Cleans up Test table from previously failed tests
    teardown_test_db()

    # Create a Test table
    cm.database.create_tables([
        cm.Test_Customer
    ])
    cm.database.close()


def teardown_test_db():
    """
    Drops test_customer, used for teardown
    """
    cm.database.drop_tables([
        cm.Test_Customer
    ])
    cm.database.close()


def test_add_ok_customer():
    """
    sets up a new db, adds customer, runs assertions and tears down db
    """
    setup_test_db()
    add_customer(**ok_customer)
    valid_customer = Test_Customer.get(Test_Customer.customer_id==ok_customer['customer_id'])

    assert valid_customer.first_name == ok_customer['name']
    assert valid_customer.customer_id == ok_customer['customer_id']
    assert valid_customer.last_name == ok_customer['lastname']
    assert valid_customer.home_address == ok_customer['home_address']
    assert valid_customer.phone_number == ok_customer['phone_number']
    assert valid_customer.email_address == ok_customer['email_address']
    assert valid_customer.status == ok_customer['status']
    assert valid_customer.credit_limit == ok_customer['credit_limit']

    teardown_test_db()


def test_credit_limit_float():
    """
    sets up a new db, adds customer, runs assertions and tears down db
    """
    setup_test_db()
    bad_customer = dict(ok_customer)
    bad_customer['credit_limit'] = '$40'

    with pytest.raises(ValueError):
        add_customer(**bad_customer)

    teardown_test_db()


def test_get_customer():
    """
    sets up a new db, adds customer, runs assertions and tears down db
    """
    setup_test_db()
    add_customer(**ok_customer)
    valid_customer = search_customer(ok_customer['customer_id'], stage='dev')

    assert valid_customer.first_name == ok_customer['name']
    assert valid_customer.customer_id == ok_customer['customer_id']
    assert valid_customer.last_name == ok_customer['lastname']
    assert valid_customer.home_address == ok_customer['home_address']
    assert valid_customer.phone_number == ok_customer['phone_number']
    assert valid_customer.email_address == ok_customer['email_address']
    assert valid_customer.status == ok_customer['status']
    assert valid_customer.credit_limit == ok_customer['credit_limit']

    teardown_test_db()


def test_delete_customer():
    """
    sets up a new db, adds customer, runs assertions and tears down db
    """
    setup_test_db()

    # Add and assert to confirm record exists before deleting
    add_customer(**ok_customer)
    valid_customer = search_customer(ok_customer['customer_id'], stage='dev')

    assert valid_customer.first_name == ok_customer['name']
    assert valid_customer.customer_id == ok_customer['customer_id']
    assert valid_customer.last_name == ok_customer['lastname']
    assert valid_customer.home_address == ok_customer['home_address']
    assert valid_customer.phone_number == ok_customer['phone_number']
    assert valid_customer.email_address == ok_customer['email_address']
    assert valid_customer.status == ok_customer['status']
    assert valid_customer.credit_limit == ok_customer['credit_limit']

    delete_customer(ok_customer['customer_id'], stage='dev')
    valid_customer = search_customer(ok_customer['customer_id'], stage='dev')

    assert valid_customer is False

    teardown_test_db()


def test_update_customer_credit():
    setup_test_db()
    add_customer(**ok_customer)
    valid_customer = search_customer(ok_customer['customer_id'], stage='dev')

    assert valid_customer.first_name == ok_customer['name']
    assert valid_customer.customer_id == ok_customer['customer_id']
    assert valid_customer.last_name == ok_customer['lastname']
    assert valid_customer.home_address == ok_customer['home_address']
    assert valid_customer.phone_number == ok_customer['phone_number']
    assert valid_customer.email_address == ok_customer['email_address']
    assert valid_customer.status == ok_customer['status']
    assert valid_customer.credit_limit == ok_customer['credit_limit']

    update_customer_credit(valid_customer.customer_id, 90210, stage='dev')
    valid_customer = search_customer(ok_customer['customer_id'], stage='dev')

    assert valid_customer.credit_limit == 90210

    # drop db
    teardown_test_db()


def test_list_active_customer():
    """
    sets up a new db, adds customers, runs assertions and tears down db
    """
    setup_test_db()
    customer_jae = dict(ok_customer)
    customer_bob = dict(ok_customer)
    customer_erin = dict(ok_customer)

    customer_jae['status'] = True
    customer_jae['name'] = 'Jae'
    customer_jae['customer_id'] = 0
    customer_erin['status'] = True
    customer_erin['name'] = 'Erin'
    customer_erin['customer_id'] = 1
    customer_bob['status'] = False
    customer_bob['name'] = 'Bob'
    customer_bob['customer_id'] = 2

    # Add 3 customers to DB, only first two are Status = True
    add_customer(**customer_jae)
    add_customer(**customer_erin)
    add_customer(**customer_bob)

    # list_active_customers - Returns a dict with 2 results
    active_customers = list_active_customers(stage='dev')

    # assert first two rows are Jae and Erin
    assert active_customers[0]['first_name'] == customer_jae['name']
    assert active_customers[1]['first_name'] == customer_erin['name']

    # drop db
    teardown_test_db()

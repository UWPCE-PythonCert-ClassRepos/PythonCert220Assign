import pytest
import customers_model as cm
import basic_operations as bo

ok_customer1 = {'customer_id': 'W3434fd',
                'first_name': 'Suzie',
                'last_name': 'Edgar',
                'home_address': '123 Browncroft Blvd, Rochester, NY 97235',
                'phone_number': '234-123-4567',
                'email_address': 'suzie@hotmail.com',
                'status': True,
                'credit_limit': 40}


ok_customer2 = {'customer_id': '2',
                'first_name': 'Chris',
                'last_name': 'Seefeld',
                'home_address': '301 Boston Commons Way, Salem, 98028',
                'phone_number': '123-456-4566',
                'email_address': 'Chris@hotmail.com',
                'status': True,
                'credit_limit': 200}


ok_customer3 = {'customer_id': '3',
                'first_name': 'Ryan',
                'last_name': 'Fermstad',
                'home_address': '808 Honolulu Way, Dimond Head, 80808',
                'phone_number': '765-432-1234',
                'email_address': 'fermy@aol.com',
                'status': False,
                'credit_limit': 300.00}


def clear_database():
    cm.database.drop_tables([
        cm.Customer
    ])
    cm.database.close()


def create_empty_database():
    clear_database()
    cm.database.create_tables([
        cm.Customer
    ])
    cm.database.close()


def test_add_customer():
    create_empty_database()
    bo.add_customer(**ok_customer1)

    test_customer = cm.Customer.get(cm.Customer.customer_id == ok_customer1['customer_id'])
    assert test_customer.first_name == ok_customer1['first_name']
    assert test_customer.last_name == ok_customer1['last_name']
    assert test_customer.home_address == ok_customer1['home_address']
    assert test_customer.email_address == ok_customer1['email_address']
    assert test_customer.status == ok_customer1['status']

    bo.add_customer(**ok_customer2)

    test_customer = cm.Customer.get(cm.Customer.customer_id == ok_customer2['customer_id'])
    assert test_customer.first_name == ok_customer2['first_name']
    assert test_customer.last_name == ok_customer2['last_name']
    assert test_customer.home_address == ok_customer2['home_address']
    assert test_customer.email_address == ok_customer2['email_address']
    assert test_customer.status == ok_customer2['status']

    clear_database()


def test_credit_limit_float():
    bad_customer = dict(ok_customer1)
    bad_customer['credit_limit'] = '$40'

    with pytest.raises(ValueError):
        bo.add_customer(**bad_customer)


def test_search_customer():
    create_empty_database()
    bo.add_customer(**ok_customer3)
    bo.search_customer(**ok_customer3)
    test_customer = cm.Customer.get(cm.Customer.customer_id==ok_customer3['customer_id'])

    assert test_customer.customer_id == ok_customer3['customer_id']
    assert test_customer.first_name == ok_customer3['first_name']
    assert test_customer.email_address == ok_customer3['email_address']
    assert test_customer.status == ok_customer3['status']
    assert test_customer.credit_limit == ok_customer3['credit_limit']

    clear_database()


def test_customer_non_existent():
    create_empty_database()

    assert bo.search_customer('5') == {}


def test_delete_customer():
    create_empty_database()
    bo.add_customer(**ok_customer3)
    bo.delete_customer(cm.Customer.get(cm.Customer.customer_id == ok_customer3['customer_id']))

    customer_deleted = bo.search_customer(ok_customer3['customer_id'])

    assert customer_deleted == {}
    clear_database()


def test_update_customer_credit():
    create_empty_database()
    bo.add_customer(**ok_customer2)

    bo.update_customer_credit("2", "700")
    updated_customer = cm.Customer.get(cm.Customer.customer_id == "2")

    assert float(updated_customer.credit_limit) == "700"

    clear_database()


def test_list_active_customers():
    create_empty_database()

    assert bo.list_active_customers() == 2

    clear_database()

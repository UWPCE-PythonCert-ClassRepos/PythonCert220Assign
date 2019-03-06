
# import os
# import peewee
import basic_operations as bo
import customers_model as cm
import pytest
import csv
import pprint

CUSTOMER_1 = {'customer_id': 'WHi32145',
              'first_name': 'Daniel',
              'last_name': 'Thomas',
              'home_address': '23 Jackson Avenue, Seattle, WA, 98122',
              'phone_number': '205-123-2334',
              'email_address': 'Daniel.Thomas@yay.com',
              'status': False,
              'credit_limit': 40.0
              }

CUSTOMER_2 = {'customer_id': 'W54Hi66',
              'first_name': 'Cho',
              'last_name': 'Asfaw',
              'home_address': '123 S LakeCity way, Seattle, WA, 98121',
              'phone_number': '232-322-1886',
              'email_address': 'cho.asfaw@uw.edu',
              'status': True,
              'credit_limit': 80.0
            }

CUSTOMER_3 = {'customer_id': 'OO4Hi66',
              'first_name': 'Habtamu',
              'last_name': 'H',
              'home_address': '123 S Jackson, Seattle, WA, 98112',
              'phone_number': '123-322-1886',
              'email_address': 'Habtamu.asfaw@uw.edu',
              'status': True,
              'credit_limit': 180.0
            }


def drop_db():
    cm.database.drop_tables(
        [cm.Customer]
    )
    cm.database.close()


def create_db():
    drop_db()
    cm.database.create_tables(
        [cm.Customer]
    )
    cm.database.close()


def test_read_csv():
    """
    read a csv
    """
    customer_data = [
        ('A000000', 'Habtamu', 'Asfaw', '3st 45th ave, Sea, wa 98122', '123-322-4321', 'cho@uw.edu', 'Active', '740'),
        ('A000001', 'cho', 'mr', '1st 5th ave, Sea, wa 98102', '321-322-4321', 'mrcho@uw.edu', 'Active', '700')
        ]
    print("Write csv file")
    with open('lesson04_assignment_data_customer.csv', 'w', encoding="ISO-8859-1") as data_customer:
        customerwriter = csv.writer(data_customer)
        customerwriter.writerow(customer_data)


    print("Read csv file back")
    with open('lesson04_assignment_data_customer.csv', 'r', encoding="ISO-8859-1") as data_customer:
        customer_reader = csv.reader(data_customer, delimiter=',', quotechar='"')
        for row in customer_reader:
            pprint.pprint(row)


def test_add_customer():
    create_db()
    bo.add_customer(**CUSTOMER_1)
    bo.add_customer(**CUSTOMER_2)
    bo.add_customer(**CUSTOMER_3)

    test_customer1 = cm.Customer.get(cm.Customer.customer_id == CUSTOMER_1['customer_id'])
    assert test_customer1.first_name == CUSTOMER_1['first_name']
    assert test_customer1.email_address == CUSTOMER_1['email_address']

    test_customer2 = cm.Customer.get(cm.Customer.customer_id == CUSTOMER_2['customer_id'])
    assert test_customer2.first_name == CUSTOMER_2['first_name']
    assert test_customer2.email_address == CUSTOMER_2['email_address']

    test_customer3 = cm.Customer.get(cm.Customer.customer_id == CUSTOMER_3['customer_id'])
    assert test_customer3.first_name == CUSTOMER_3['first_name']
    assert test_customer3.email_address == CUSTOMER_3['email_address']

    drop_db()


def create_customer_db():
    drop_db()
    cm.database.create_tables([
        cm.Customer
    ])
    bo.add_customer(**CUSTOMER_1)
    bo.add_customer(**CUSTOMER_2)
    bo.add_customer(**CUSTOMER_3)
    cm.database.close()


def test_credit_limit_float():
    create_customer_db()
    bad_customer = dict(CUSTOMER_1)
    bad_customer['credit_limit'] = '$40'

    with pytest.raises(ValueError):
        bo.add_customer(**bad_customer)

    drop_db()


def test_search_for_customer_exists():
    create_customer_db()
    test_customer = bo.search_customer('OO4Hi66')
    assert test_customer['first_name'] == CUSTOMER_3['first_name']
    assert test_customer['last_name'] == CUSTOMER_3['last_name']
    assert test_customer['email_address'] == CUSTOMER_3['email_address']
    assert test_customer['phone_number'] == '123-322-1886'

    drop_db()


def test_search_for_customer_not_exist():
    create_customer_db()
    assert bo.search_customer('32145') == dict()

    drop_db()


def test_delete_customer():
    create_customer_db()
    bo.delete_customer(cm.Customer.get(cm.Customer.customer_id == CUSTOMER_1['customer_id']))

    deleted = bo.search_customer(CUSTOMER_1['customer_id'])
    assert deleted == {}

    drop_db()


def test_delete_customer_count():
    create_customer_db()
    number_of_customers = (cm.Customer.select().count())
    assert number_of_customers == 3

    bo.delete_customer("W54Hi66")

    current_number_of_customers = (cm.Customer.select().count())
    assert current_number_of_customers == 2

    drop_db()


def test_list_active_customers():
    create_customer_db()
    # list_active_customers = cm.Customer.get(cm.Customer.customer_id == CUSTOMER_1['customer_id'])
    # assert bo.list_active_customers. == 0
    for customer in bo.list_active_customers():
        assert customer in ['W54Hi66', 'OO4Hi66']
    drop_db()


def test_update_customer_credit_limit_exists():
    create_customer_db()

    test_customer1 = cm.Customer.get(cm.Customer.customer_id == 'W54Hi66')
    assert test_customer1.credit_limit == 80.0

    bo.update_customer_credit('W54Hi66', 801.0)
    test_customer2 = cm.Customer.get(cm.Customer.customer_id == 'W54Hi66')
    assert test_customer2.credit_limit == 801.0

    drop_db()


def test_integration():
    # Add customer records
    create_customer_db()
    # bo.add_customer(**CUSTOMER_1)
    # bo.add_customer(**CUSTOMER_2)

    # Delete customer records
    bo.delete_customer(CUSTOMER_1["customer_id"])

    # Update customer credit limit record
    bo.update_customer_credit("W54Hi66", 500.0)
    update_customer = cm.Customer.get(cm.Customer.customer_id == "W54Hi66")
    assert update_customer.credit_limit == 500.0

    # Search customer records
    create_customer_db()
    test_customer = bo.search_customer('WHi32145')
    assert test_customer['first_name'] == CUSTOMER_1['first_name']

    # List active customers
    list_active_customers = cm.Customer.get(cm.Customer.customer_id == CUSTOMER_1['customer_id'])
    assert list_active_customers.status == 0
    # assert bo.list_active_customers() == 1

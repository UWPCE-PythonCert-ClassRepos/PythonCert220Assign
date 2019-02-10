from basic_operations import add_customer
from basic_operations import search_customer
from basic_operations import delete_customer
from basic_operations import update_customer
from basic_operations import list_active_customers

from customer_model import Customer
import pytest

ok_customer = {
    'customer_id': 'W3434fd',
    'first_name': 'Suzie',
    'last_name': 'Edgar',
    'home_address': '123 Browncroft Blvd, Rochester, NY 97235',
    'phone_number': '234-123-4567',
    'email_address': 'suzie@hotmail.com',
    'status': True,
    'credit_limit': '40'
}


def add_second_customer():
    second_customer = dict(ok_customer)
    second_customer["customer_id"] = "W3434ff"
    second_customer["first_name"] = "Bob"
    second_customer["email_address"] = 'bob@hotmail.com'
    add_customer(**second_customer)
    return second_customer


def add_third_customer():
    third_customer = dict(ok_customer)
    third_customer["customer_id"] = "M3233bb"
    third_customer["first_name"] = "Jackson"
    third_customer["status"] = False
    add_customer(**third_customer)
    return third_customer


def add_fourth_customer():
    fourth_customer = dict(ok_customer)
    fourth_customer["customer_id"] = "M3233cc"
    fourth_customer["first_name"] = "Michael"
    fourth_customer["status"] = False
    add_customer(**fourth_customer)
    return fourth_customer


def clean_up(customer_id):
    test_customer = Customer.get(Customer.customer_id == customer_id)
    test_customer.delete_instance()


def test_add_ok_customer():
    add_customer(**ok_customer)
    test_customer = Customer.get(
        Customer.customer_id == ok_customer['customer_id'])
    assert test_customer.email_address == ok_customer['email_address']
    assert test_customer.customer_id == ok_customer['customer_id']
    assert test_customer.first_name == ok_customer['first_name']
    assert test_customer.last_name == ok_customer['last_name']
    assert test_customer.phone_number == ok_customer['phone_number']
    assert test_customer.home_address == ok_customer['home_address']
    assert test_customer.status == ok_customer['status']
    assert test_customer.credit_limit == float(ok_customer["credit_limit"])
    clean_up(ok_customer['customer_id'])


def test_credit_limit_float():
    bad_customer = dict(ok_customer)
    bad_customer['credit_limit'] = '$40'

    with pytest.raises(ValueError):
        add_customer(**bad_customer)


def test_add_multiple_customers():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    test_customer = Customer.get(
        Customer.customer_id == ok_customer['customer_id'])
    test_customer1 = Customer.get(
        Customer.customer_id == second_customer["customer_id"])
    assert test_customer != test_customer1
    assert test_customer.first_name == 'Suzie'
    assert test_customer1.first_name == 'Bob'
    clean_up(ok_customer["customer_id"])
    clean_up(second_customer["customer_id"])


def test_search_customer():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    customer_dict = search_customer("W3434ff")
    second_customer["credit_limit"] = float(second_customer["credit_limit"])
    assert customer_dict == second_customer
    clean_up(ok_customer["customer_id"])
    clean_up(second_customer["customer_id"])


def test_search_customer_null():
    add_customer(**ok_customer)
    customer_dict = search_customer("12345")
    assert customer_dict == {}
    customer_dict = search_customer(7)
    assert customer_dict == {}
    customer_dict = search_customer()
    assert customer_dict == {}
    clean_up(ok_customer["customer_id"])


def test_delete_customer():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    delete_customer(second_customer["customer_id"])
    customer_dict = search_customer(second_customer["customer_id"])
    assert customer_dict == {}
    ok_customer["credit_limit"] = float(ok_customer["credit_limit"])
    customer_dict = search_customer(ok_customer["customer_id"])
    assert customer_dict == ok_customer
    clean_up(ok_customer['customer_id'])


def test_delete_not_a_customer():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    delete_customer("12345")
    delete_customer(7)
    delete_customer()
    clean_up(ok_customer['customer_id'])
    clean_up(second_customer['customer_id'])


def test_update_customer_credit():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    update_customer(
        customer_id=second_customer["customer_id"], credit_limit=100.0)
    customer_dict = search_customer(second_customer["customer_id"])
    assert customer_dict["credit_limit"] == 100.0
    clean_up(ok_customer['customer_id'])
    clean_up(second_customer['customer_id'])


def test_update_customer_credit_no_match():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    with pytest.raises(ValueError):
        update_customer(customer_id="12345", credit_limit=100.0)
    clean_up(ok_customer['customer_id'])
    clean_up(second_customer['customer_id'])


def test_list_active_customers():
    add_customer(**ok_customer)
    second_customer = add_second_customer()
    third_customer = add_third_customer()
    fourth_customer = add_fourth_customer()
    active_customers = list_active_customers()
    assert active_customers == 2
    test_customer3 = Customer.get(
        Customer.customer_id == third_customer["customer_id"])
    test_customer3.status = True
    test_customer3.save()
    active_customers = list_active_customers()
    assert active_customers == 3
    clean_up(ok_customer['customer_id'])
    clean_up(second_customer['customer_id'])
    clean_up(third_customer['customer_id'])
    clean_up(fourth_customer['customer_id'])

from basic_operations import (add_customer, search_customer, delete_customer,
update_customer_credit, list_active_customers, bulk_add_customers)
from customer_model import Customer
import pytest
import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"

logging.basicConfig(level=logging.INFO, format=log_format,
                    filename='db.log')

def test_bulk_add_customers_bad():

    with pytest.raises(FileNotFoundError):
        bulk_add_customers('fake.csv')

def test_bulk_add_customers_good():
    # Clear database
    Customer.delete().where(Customer.customer_id)

    bulk_add_customers('data.csv')

    custs = Customer.select()

    assert custs.count() > 0


def test_add_customer():
    customer_id = "000001"
    first_name = "Oboe"
    last_name = "Nome"
    home_address = "22 Avenue"
    phone_number = "832-294-2929"
    email_address = "dog@dog.com"
    status = True
    credit_limit = 1000

    add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit)

    cust = Customer.get(Customer.customer_id == customer_id)

    assert cust.home_address == "22 Avenue"


def test_search_customer():

    cust = search_customer("000001")

    assert cust['email_address'] == "dog@dog.com"


def test_bad_search_customer():

    cust = search_customer("12947242")

    assert cust == {}


def test_update_customer_credit():

    update_customer_credit("000001", 10000)
    try:
        cust = Customer.get(Customer.customer_id == "000001")
        assert cust.credit_limit == 10000
    except Exception as e:
        logging.info(e)
        raise ValueError
        assert True


def test_list_active_customers():

    result = list_active_customers()
    logging.info(result)
    assert result == 8


def test_delete_customer():

    delete_customer("000001")

    with pytest.raises(Exception) as e:
        logging.info(e)
        Customer.get(Customer.customer_id == "000001")

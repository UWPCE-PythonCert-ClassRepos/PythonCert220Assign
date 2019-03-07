"""
Test inventory file for adding furniture and returning an invoice
"""
import os
import pytest
from inventory import add_furniture, single_customer

INVOICE_FILE = 'test_items.csv'

def remove_file(file):
    try:
        os.remove(file)
    except OSError:
        pass

@pytest.fixture(scope="function")
def setup_invoice_file(request):
    add_furniture(INVOICE_FILE, "Elisa Miles", "LR04", "Leather Sofa", 25.00)
    add_furniture(INVOICE_FILE, "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture(INVOICE_FILE, "Alex Gonzales", "Queen Matress", 17)
    add_furniture(INVOICE_FILE, "Elisa Miles", "Queen Matress", 17.00)

    def teardown():
        remove_file(INVOICE_FILE)
    request.addfinalizer(teardown)

def test_add_furniture_create_file():
    remove_file(INVOICE_FILE)
    add_furniture(INVOICE_FILE)
    assert os.path.isfile(INVOICE_FILE)
    remove_file(INVOICE_FILE)

def test_add_furniture_data(setup_invoice_file):
    line_count = sum(1 for line in open(INVOICE_FILE))
    assert line_count == 4

def test_single_customer_good(setup_invoice_file):
    elisa_invoice_csv = 'Elisa_Miles_invoice.csv'
    create_invoice = single_customer('Elisa Miles', elisa_invoice_csv)
    create_invoice(INVOICE_FILE)
    line_count = sum(1 for line in open(elisa_invoice_csv))
    assert line_count == 2
    remove_file(elisa_invoice_csv)

def test_single_customer_bad(setup_invoice_file):
    non_customer_csv = 'non_customer.csv'
    create_invoice = single_customer("Non Customer", non_customer_csv)
    create_invoice(INVOICE_FILE)
    line_count = sum(1 for line in open(non_customer_csv))
    assert line_count == 0
    remove_file(non_customer_csv)

import os
import pytest
import inventory_v1 as inv

INVOICE_FILE = 'test_invoice_file.csv'
RENTAL_FILE = 'test_items.csv'

def remove_file(file):
    try:
        os.remove(file)
    except OSError:
        pass

@pytest.fixture(scope='function')
def setup_invoice_file(request):
    inv.add_furniture(INVOICE_FILE, 'Emilia', 'ELR04', 'Leather Sofa', 250.00)

    def teardown():
        remove_file(INVOICE_FILE)
    request.addfinalizer(teardown)

def test_add_furniture():
    remove_file(INVOICE_FILE)
    inv.add_furniture(INVOICE_FILE, 'Emilia', 'LR04', 'Sofa', 50.00)
    inv.add_furniture(INVOICE_FILE, 'John', 'PS60', 'Chair', 150.00)
    
    assert os.path.isfile(INVOICE_FILE)
    with open(INVOICE_FILE, 'r') as csv_invoice:
        rows = csv_invoice.readlines()
        assert rows[0] == "Emilia, LR04, Sofa, 50.00\n"
        assert rows[1] == "John, PS60, Chair, 150.00\n"

        assert len(rows) == 2

    remove_file(INVOICE_FILE)

def test_single_customer():
    customer_file = inv.single_customer("Lisa Miles", INVOICE_FILE)
    customer_file(RENTAL_FILE)
    with open(INVOICE_FILE, 'r') as file:
        items = file.readlines()
        assert items[0] == "Lisa Miles, LR04, Leather Sofa, 25.00\n"
        assert len(items) == 2

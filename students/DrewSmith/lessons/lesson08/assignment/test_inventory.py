'''
Tests the inventory functions
'''


from pytest import fixture
import inventory
import os

@fixture(autouse=True)
def setup_teardown():
    ''' Fixture to execute before and after tests '''
    if os.path.exists('test_invoices.csv'):
        os.remove('test_invoices.csv')
    yield


def test_add_furniture():
    inventory.add_furniture("test_invoices.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    with open('test_invoices.csv', 'r') as file:
        lines =  file.readlines()
        assert len(lines) == 1
        assert lines[0] == "Elisa Miles,LR04,Leather Sofa,25\n"

def test_add_furniture_append():
    inventory.add_furniture("test_invoices.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    inventory.add_furniture("test_invoices.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    with open('test_invoices.csv', 'r') as file:
        lines =  file.readlines()
        assert len(lines) == 2
        assert lines[0] == "Elisa Miles,LR04,Leather Sofa,25\n"
        assert lines[1] == "Edward Data,KT78,Kitchen Table,10\n"

def test_single_customer():
    result = inventory.single_customer("test_invoices.csv", "Fresh Prince")
    result("test_items.csv")
    with open('test_invoices.csv', 'r') as file:
        lines =  file.readlines()
        assert len(lines) == 3
        assert lines[0] == "Fresh Prince,LR04,Leather Sofa,25.00\n"
        assert lines[1] == "Fresh Prince,KT78,Kitchen Table,10.00\n"
        assert lines[2] == "Fresh Prince,BR02,Queen Mattress,17.00\n"

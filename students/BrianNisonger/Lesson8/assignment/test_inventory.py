from inventory import add_furniture
from inventory import single_customer
import pytest
from contextlib import contextmanager
import csv


@contextmanager
def does_not_raise():
    yield


@pytest.fixture
def test_single_customer_results():
    return [["Susan Wong", "LR04", "Leather Sofa", "25.00"],
            ["Susan Wong", "KT78", "Kitchen Table", "10.00"],
            ["Susan Wong", "BR02", "Queen Mattress", "17.00"],
            ["Susan Wong", "AA01", "Monkey Wrench", "18.00"],
            ["Susan Wong", "JMLL", "Pumpkin Head", "19.00"]]


@pytest.mark.parametrize(
    "test_input,expected,expectation",
    [(("invoice01.csv", "Elisa Miles", "LR04", "Leather Sofa", 25),
      b'Elisa Miles,LR04,Leather Sofa,25.00\r\r\n', does_not_raise()),
     (("invoice01.csv", "Edward Data", "KT78", "Kitchen Table", 10),
      b'Edward Data,KT78,Kitchen Table,10.00\r\r\n', does_not_raise()),
     (("invoice01.csv", "Alex Gonzales", "Queen Mattress", 17), None,
      pytest.raises(IndexError)),
     (("invoice01.csv", "Elisa Miles", "LR04", "Leather Sofa", "a"), None,
      pytest.raises(ValueError))])
      
def test_add_furniture(test_input, expected, expectation):
    with expectation:
        add_furniture(*test_input)
        with open(test_input[0], 'rb') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
            assert expected == last_line


def test_single_customer(test_single_customer_results):
    create_invoice = single_customer("Susan Wong", "SW_invoice.csv")
    create_invoice("test_items.csv")
    with open("test_items.csv", mode="r") as customer_file:
        customer_reader = csv.reader(customer_file)
        customer_list = [row for row in customer_reader]
    assert customer_list[0] == test_single_customer_results[0]

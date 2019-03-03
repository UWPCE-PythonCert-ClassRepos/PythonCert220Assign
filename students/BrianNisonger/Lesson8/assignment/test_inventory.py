from inventory import add_furniture
from inventory import single_customer
import pytest
from contextlib import contextmanager
import csv

@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize("test_input,expected,expectation",[
(("invoice01.csv", "Elisa Miles", "LR04", "Leather Sofa", 25),("Elisa Miles", "LR04", "Leather Sofa", "25.00"),does_not_raise()),
(("invoice01.csv", "Edward Data", "KT78", "Kitchen Table", 10),("Edward Data", "KT78", "Kitchen Table", "10.00"),does_not_raise()),
(("invoice01.csv", "Alex Gonzales", "Queen Mattress", 17),(),pytest.raises(IndexError))
])




def test_add_furniture(test_input,expected,expectation):
    with expectation:
        add_furniture(*test_input)
        a=open(test_input[0],'rb')
        lines=a.readlines()
        if lines:
            last_line = lines[-1]
        print(last_line)    
        assert False
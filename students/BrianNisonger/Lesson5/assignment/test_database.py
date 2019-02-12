import os
import pytest

from database import import_data

@pytest.fixture
def _show_available_products():
    return
    {
     
    }

@pytest.fixture    
def _show_rentals():
    return 
    {
     
    }

    
def test_import_data():
    added,error = import_data("dat","product_data.csv","customer_data.csv","rental_data.csv")
    print(added)
    print(error)
    assert False
    
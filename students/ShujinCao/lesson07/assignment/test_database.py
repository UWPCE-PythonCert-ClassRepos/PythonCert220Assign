import linear as db
import pytest

def test_import():
    results = db.list_available_products()
    assert [*results] ==['prd001', 'prd003', 'prd004', 'prd005', 'prd006', 'prd008',
                  'prd010']

def test_list_renter_info():
    results = db.list_renter_info("prd005")
    assert [*results] == ['user001', 'user003']


def test_list_available_products():
    results = db.list_available_products()
    assert [k for k in results.values()][4]['description'] == 'Portable heater'

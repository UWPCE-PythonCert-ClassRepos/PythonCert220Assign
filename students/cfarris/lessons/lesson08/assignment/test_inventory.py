#!/usr/bin/env Python3

'''
Test inventory.py
'''
import os.path
from inventory import add_furniture, single_customer


def test_add_furniture(tmpdir):
    '''
    tests add_furniture function from inventory.py
    '''
    invoice_file = tmpdir.join("test_invoice_file.csv")
    add_furniture('LR04',
                  'Leather Sofa',
                  25.00,
                  invoice_file.strpath,
                  'Elisa Miles')
    assert os.path.isfile(invoice_file) == True
    with open(invoice_file.strpath, 'r') as i_file:
        results = i_file.read()
        assert results == 'Elisa Miles, LR04, Leather Sofa, 25.0\n'


def test_single_customer(tmpdir):
    '''
    tests single_customer function from inventory.py
    '''
    invoice_file = tmpdir.join("test_invoice_file2.csv")
    rentals_to_invoice = single_customer('Mrs. McSpendy', invoice_file.strpath)
    client_file = 'test_client_items.csv'
    rentals_to_invoice(client_file)
    with open(invoice_file.strpath, 'r') as f_file:
        results = f_file.read()
    assert results == 'Mrs. McSpendy, aTeST, Leather Sofa, 25.00\nMrs. McSpendy, bTeSt, Kitchen Table, 10.00\n'

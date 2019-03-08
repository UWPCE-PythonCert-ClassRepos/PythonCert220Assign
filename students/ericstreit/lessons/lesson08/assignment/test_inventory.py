#!/usr/bin/env python3
#import stuff here
from functools import partial
import inventory

def test_partial():
    king_kong = partial(inventory.single_customer_partial, new_invoice_file =
                        'king_kong_invoice.csv')
    assert king_kong('King Kong') == 'Invoice king_kong_invoice.csv created for King Kong.'

def test_closure():
    godzilla = inventory.single_customer('Godzilla')
    assert godzilla('godzilla_invoice.csv') == 'Invoice godzilla_invoice.csv created for Godzilla.'

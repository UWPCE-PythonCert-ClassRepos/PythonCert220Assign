from unittest import TestCase
import os
import csv
from builtins import RuntimeError

import config
import basic_operations as bs
from customer_model import Customer, create_cust_table, delete_cust_table, database

# other tests I would add:
# make sure inactive works, so if I add inactive customers, I can get them and only them back.
# probably should add inactive customers when checking active customers, for that matter. As is,
# could just be giving back the whole list, no matter what and we would not know.
# error checking: is status really a boolean is probably important. other stuff may not be so
# important until we know what they are going to do with the data

class TestCustomer(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Connect to the database and create our table
        """
        if config.TEST_DATABASE is not config.DATABASE:
            raise RuntimeError("Datatbase names do not match, fix your configuration")
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
        create_cust_table()
        # add a bunch of customers to make sure works with non-empty database
        # maybe change this so it isn't quite so many, tests take too long now
        bs.add_from_csv('customer.csv')
        cls.active_cust_csv = get_count('customer.csv')

    @classmethod
    def tearDownClass(cls):
        # easy way, since it is a test database. :)
        os.remove(config.TEST_DATABASE)

    def setUp(self):
        """
        Add one customer to be available for most operations
        """
        # really should add more customers to this
        # maybe add a mass-add customers function in basic_operations
        bs.add_customer(**config.customer1)

    def tearDown(self):
        """
        Remove customers from config so can start again (won't always have both)
        """
        for customer in (config.customer1, config.customer2):
            try:
                bs.delete_customer(customer['customer_id'])
            except ValueError:
                pass

    def test_add_customer(self):
        bs.add_customer(**config.customer2)
        cust = Customer.get(Customer.customer_id == config.customer2['customer_id'])
        self.assertEqual(cust.home_address, config.customer2['home_address'])

    def test_add_customer_incomplete_data(self):
        bad_cust = 'elmer fudd'
        with self.assertRaises(ValueError) as exc:
            bs.add_customer(bad_cust)
        # problem was I couldn't add a message to a key error, so changed
        # from keyerror to valueerror
        self.assertEqual(str(exc.exception), config.etext['no_save'].format(bad_cust))

    def test_customer_status_wrong(self):
        with self.assertRaises(ValueError) as exc:
            bs.add_customer(**config.bad_customer)
        self.assertEqual(str(exc.exception),
                         config.etext['req_bool'].format(config.bad_customer['status']))

    def test_search_customer(self):
        cust = bs.search_customer(config.customer1['customer_id'])
        self.assertEqual(cust['email_address'], config.customer1['email_address'])

    def test_bad_search_customer(self):
        cust = bs.search_customer("12947242")
        self.assertEqual(cust, {})

    def test_update_customer_credit(self):
        bs.update_customer_credit(config.customer1['customer_id'], 10000)
        cust = Customer.get(Customer.customer_id == config.customer1['customer_id'])
        self.assertEqual(cust.credit_limit, 10000)

    def test_list_active_customers(self):
        result = bs.list_active_customers()
        exp_result = 1 + self.active_cust_csv
        self.assertEqual(result, exp_result)

    def test_delete_customer(self):
        bs.delete_customer(config.customer1['customer_id'])
        with self.assertRaises(Exception):
            Customer.get(Customer.customer_id == config.customer1['customer_id'])

    def test_delete_unknown_customer(self):
        unk_id = 'supercalifragilisticex'
        with self.assertRaises(Exception) as exc:
            bs.delete_customer(unk_id)
        self.assertEqual(str(exc.exception), config.etext['not_found'].format(unk_id))


def get_count(csv_file):
    """ Make sure what we count in the file is what the database says is true"""
    count = 0
    with open('customer.csv', 'r', newline='', encoding='ISO-8859-1') as myfile:
        for row in csv.reader(myfile):
            if row[6].lower() == 'active':
                count += 1
    return count

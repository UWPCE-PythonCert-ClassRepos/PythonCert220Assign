from unittest import TestCase
import os

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
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
        create_cust_table()

    @classmethod
    def tearDownClass(cls):
        # easy way, since it is a test database. :)
        os.remove(config.TEST_DATABASE)

    def setUp(self):
        """
        Add one customer to be available for most operations
        """
        # really should add more customers to this
        bs.add_customer(**config.customer1)

    def tearDown(self):
        """
        Remove all customers so can start again
        """
        delete_cust_table() # changed where I put this. now it is in customer_model,
        # where users are unlikely to have access, so doesn't have to be private

    def test_add_customer(self):
        bs.add_customer(**config.customer2)
        cust = Customer.get(Customer.customer_id == config.customer2['customer_id'])
        self.assertEqual(cust.home_address, config.customer2['home_address'])

    def test_add_customer_incomplete_data(self):
        bad_cust = 'elmer fudd'
        with self.assertRaises(Exception) as exc:
            bs.add_customer(bad_cust)
        # I really wanted to raise a different exception instead,
        # but this test hated that.
        self.assertEqual(str(exc.exception), "'first_name'")

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
        self.assertEqual(result, 1)

    def test_delete_customer(self):
        bs.delete_customer(config.customer1['customer_id'])
        with self.assertRaises(Exception):
            Customer.get(Customer.customer_id == config.customer1['customer_id'])

    def test_delete_unknown_customer(self):
        unk_id = 'supercalifragilisticex'
        with self.assertRaises(Exception) as exc:
            bs.delete_customer(unk_id)
        self.assertEqual(str(exc.exception), config.etext['not_found'].format(unk_id))

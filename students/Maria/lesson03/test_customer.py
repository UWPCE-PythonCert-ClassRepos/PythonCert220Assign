from unittest import TestCase
import os

import config
import basic_operations as bs
from customer_model import Customer, create_tables


class TestCustomer(TestCase):

    @classmethod
    def setUpClass(cls):
        create_tables()

    @classmethod
    def tearDownClass(cls):
        # easy way. :)
        os.remove(config.TEST_DATABASE)

    def setUp(self):
        """
        Add one customer to be available for most operations
        """
        bs.add_customer(**config.customer1)

    def tearDown(self):
        """
        Remove all customers so can start again
        """
        bs._delete_table()

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

""" Jean-Baptiste@Seattle 02/20/2019
This is my project 04 we are going to apply the functional programming techniques
we have learned to improve code that we have written in earlier lessons for the case study.
As important as learning the syntax for iterables, iterators and generators is understanding
the context in which they are best used.
"""
import peewee as pw
import logging
import csv
from customers_model import database, Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
data = []
with open('customer.csv',  'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    for line in reader:
        line['id'] = float(line['id'])
        line['first_name'] = string(first_name)
        line['last_name'] = string(last_name)
        line['home_address'] = string(home_address)
        line['email_address'] = string(email_address)
        line['phone_number'] = integer(phone_number)
        line['status'] = string(status)
        line['credit_limit'] = string(credit_limit)
        data.append(line)

my_attrs = ['id','first_name', 'last_name', 'email_address', 'phone_number','status','credit_limit']
''' This is to create customer table'''
csv.DictReader(f, delimiter=',')
model.add_csv('customer.csv')
clsm.active_customer_csv=get_count('customer.csv')
@classmethod
#"This is to add a new customer"
def modelClass(cls):
    data.create(config.my_attrs)
    def new_customer(self):
        self.customer=customer
        customer=Customer.get(Customer.id==config.new1_customer['id'])
        database.add_new_customer(**config.new1_customer)
        for config.new1_customer in config.Test_db:
            try:
                database.add_new_customer(customer[id])
                logger.info("The new1 customer is successfully added!")
            except ValueError:
                pass
            new_customer.save()
            logging.info(f"Added {first_name} to database")
            database.close()

#"This is to test a customer"
def test_add_customer(self):
    try:
        database.add_new_customer(**config.new2_customer)
        customer=Customer.get(Customer.id==config.new2_customer['id'])
        self.assertEqual(customer.home_address,config.new2_customer['home_address'])
    except ValueError:
        pass

def reseach_customer(self):
    self.customer=customer
    output_dict={}
    try:
        customer=Custumer.get(Customer.id==id)
        output_dict={customer_attr:getattr(customer, customer_attr) for customer_attr in my_attrs}
        logging.info("customer object exists")
    except:pw.NotExist
    logging.error(err)
    return output_dict

#"This is to remove a customer"
    def delete_customer(self):
        self.delete_customer=delete_customer
        database.delete_customer(**config.customer)
        for customner in (config.new1_customer, config.new2_customer):
            try:
                database.delete_cutomer(customer[id])
                logger.info("The customer is successfully deleted!")
            except ValueError:
                pass





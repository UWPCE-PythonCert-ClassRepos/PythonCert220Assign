import peewee as pw
import logging
import csv
from customer_model import Customer

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format, filename='db.log')


def bulk_add_customers(csv_file):

    try:
        file_ = csv.DictReader(open(csv_file))
    except FileNotFoundError:
        logging.info(f"{csv_file} doesn't seem to exist")
        print(f"{csv_file} doesn't seem to exist")
        raise FileNotFoundError

    for record in file_:
        if record['status'] not in [True, False]:
            logging.info(f"{record['customer_id']} has invalid status:\
                         {record['status']}")
            print(f"Status must be True or False for {record['customer_id']}")
            pass
        else:
            cust = Customer.create(customer_id=record['customer_id'],
                                   first_name=record['first_name'],
                                   last_name=record['last_name'],
                                   home_address=record['home_address'],
                                   phone_number=record['phone_number'],
                                   email_address=record['email_address'],
                                   status=record['status'],
                                   credit_limit=record['credit_limit'])
            cust.save()
            logging.info(f'Customer {record["customer_id"]} added successfully!')

def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
    try:
        cust = Customer.create(customer_id=customer_id,
                               first_name=first_name,
                               last_name=last_name,
                               home_address=home_address,
                               phone_number=phone_number,
                               email_address=email_address,
                               status=status,
                               credit_limit=credit_limit)
        cust.save()
        logging.info("Customer successfully added!")

    except Exception as e:
        logging.info(f"Could not add {first_name} to db")
        logging.info(e)


def search_customer(customer_id):
    """
    Return a dictionary object with name, lastname, email address and phone
    number of a customer or an empty dictionary object if no customer was found
    """

    output_dict = {}

    try:
        cust = Customer.get(Customer.customer_id == customer_id)
        logging.info("Cust object exists")
        output_dict['first_name'] = cust.first_name
        output_dict['last_name'] = cust.last_name
        output_dict['email_address'] = cust.email_address
        output_dict['phone_number'] = cust.phone_number
    except Exception as e:
        logging.info(e)

    return output_dict


def delete_customer(customer_id):
    cust = Customer.get(Customer.customer_id == customer_id)
    cust.delete_instance()


def update_customer_credit(customer_id, credit_limit):
    cust = Customer.get(Customer.customer_id == customer_id)
    cust.credit_limit = credit_limit
    cust.save()


def list_active_customers():
    num_custs = Customer.select().where(Customer.status == 1)
    return num_custs.count()



import csv
import logging

def add_furniture(*args):
    with open(args[0], mode="a") as customer_file:
        customer_writer=csv.writer(customer_file) 
        try:
            customer_writer.writerow([args[1],args[2],args[3],f'{args[4]:.2f}'])
        except IndexError:
            logging.error("Missing values")
            raise(IndexError)
    return None


def single_customer():
    pass

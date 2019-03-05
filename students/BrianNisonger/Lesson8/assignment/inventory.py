import csv
import logging


def add_furniture(*args):
    with open(args[0], mode="a") as customer_file:
        customer_writer = csv.writer(customer_file)
        try:
            customer_writer.writerow(
                [args[1], args[2], args[3], f'{args[4]:.2f}'])
        except IndexError:
            logging.error("Missing values")
            raise (IndexError)
        except ValueError:
            logging.error("Not a number")
            raise (ValueError)
    return None


def single_customer(customer_name, customer_invoice_file):
    with open(customer_invoice_file, mode="r") as customer_file:
        customer_reader = csv.reader(customer_file)
        customer_list = [(customer_name, row) for row in customer_reader]

    def create_invoice(invoice_file):
        nonlocal customer_list
        with open(invoice_file, mode="a") as customer_outfile:
            customer_writer = csv.writer(customer_outfile)
            for row in customer_list:
                customer_writer.writerow(
                    [row[0], row[1][0], row[1][1], f'{float(row[1][2]):.2f}'])
        return None

    return create_invoice

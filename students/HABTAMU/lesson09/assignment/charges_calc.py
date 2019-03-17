
'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math

import logging
import traceback
import functools
import sys

def create_logger():
    """
    Creates a logging object and returns it, parse logging argument selective, by using decorators.
    conditional logging with single command line variable which can turn logging on or off for decorated classes or functions.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)
    
    # create the logging file handler, log filename format with timestamp 
    file_handler = logging.FileHandler(datetime.datetime.now().strftime(" charges_calc %Y-%m-%d") + '.log')
    file_handler.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(file_handler)

    return logger


def exception(function):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except:
            # log the exception
            err = "There was an exception in  "
            err += function.__name__
            logger.exception(err)

            # re-raise the exception
            raise
    return wrapper

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers and logging.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    # parser.add_argument('-d', required=True)
    parser.add_argument('-d', '--debug', help='enable debug logging', required=False, default=0)

    return parser.parse_args()

@exception
def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            # Error loading json from file, for the reason expected property name error out.
            logging.error("Error loading json from file {}".format(filename))
            logging.warning("JSONDecodeError: Expecting property name enclosed in double quotes: line 5884 column 23")

            # Here capture logging stacktrace or traceback to track the code’s execution error.
            logging.exception("The next few lines are Traceback error message")

            # Error out with exit(1) to failed loading json
            exit(1)
    return data

@exception
def calculate_additional_fields(data):
    """ calculates the square root of the total cost of the rental for statistical purposes,
        args: json file data as an input,
        returns: the total cost of the rental (based on the number of days the item or items have been rented), 
        as well as total cost per item (in the case of multiple items).
    """
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(
                value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(
                value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days

            # Update proper time data manually for rental_end, "rental_end": "6/19/18" to pass the script,
            logging.warning("ValueError: rental_end time data from source file is set '' which does not match format '%m/%d/%y',")
            
            # wrote another script (clean_up.py) to switch rental_start and rental_end.
            logging.error("rental_start needs to be prior to rental_end, total_days shouldn't be negative")

            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            if value['units_rented'] == 0:
                value['unit_cost'] = value['total_price']
            else:
                value['unit_cost'] = value['total_price'] / \
                    value['units_rented']
        except:
            logging.error("Error calculating input data")
            logging.exception("message")

            # Error out with exit(1), script failed unless this fields needs to be corrected.
            exit(1)

    return data

@exception
def save_to_json(filename, data):
    """ To get utf8-encoded file as opposed to ascii-encoded,
        json.dump writes to a text file, it's output is ASCII-only by default,
            args: take file name and json data as an arguments,
        
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)

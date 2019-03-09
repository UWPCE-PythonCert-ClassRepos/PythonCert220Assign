"""
Lesson 09 Assignment - Part 1
Decorators
"""


# We are going to make logging selective, by using decorators.
# Add decorator(s) to introduce conditional logging so that a single command line variable
# can turn logging on or off for decorated classes or functions.


import argparse
import json
import datetime
import math
import logging

logger = logging.getLogger(__name__)


def parse_cmd_arguments():
    """
    Parses arguments from the command line.
    :return:
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='enable debug logging', required=False, default=0)
    parser.add_argument("-l", "--limit", help="set limit of logging", required=False, default=0)

    return parser.parse_args()


def set_log_level(log_level):
    """
    Sets log level for debugger.
    :param log_level: 0, 1, 2, or 3
    """

    if log_level == 0:
        return

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler('charges_calc.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if log_level == 1:
        logger.setLevel(logging.ERROR)
    elif log_level == 2:
        logger.setLevel(logging.WARNING)
    elif log_level == 3:
        logger.setLevel(logging.DEBUG)

# def set_limit_level()


def logged_func(func):
    def logged(*args, **kwargs):

        logging.disable(logging.CRITICAL)

        result = func(*args, **kwargs)

        logging.disable(logging.NOTSET)

        return result
    return logged


def load_rentals_file(filename):
    """
    Loads rental data from the source file.
    :param filename: source file
    :return: data
    """

    logger.debug("Opening file %s", filename)
    with open(filename) as file:
        try:
            data = json.load(file)
        except ValueError as err:
            logging.error("Error reading input file %s", file)
            # print(f"Error reading the input file: {err}")
            exit(0)
    return data


@logged_func
def calculate_additional_fields(data):
    """
    Calculates additional metrics.
    :param data: Data from the source file.
    :return: additional data
    """
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as date_error:
            logger.error("%s Date format is incorrect.", date_error)
            # print(f"Date format is incorrect. Should be m/d/y.")
            logger.debug(value)

        value['total_days'] = (rental_end - rental_start).days

        if value["total_days"] < 0:
            logger.error("Total days is negative.")
            # print("Total days cannot be negative. Check rental start and end dates.")
            logger.debug(value)

        value['total_price'] = value['total_days'] * value['price_per_day']

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError as math_error:
            logger.warning("%s - Error with square root of total price.", math_error)
            # print("Error with square root of total price.")
            logger.debug(value)

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as zero_error:
            logger.warning("%s Cannot divide by 0.", zero_error)
            # print("Error with units rented. Cannot divide by 0.")
            logger.debug(value)
    return data



def save_to_json(filename, data):
    """
    Saves results to output file.
    :param filename: output filename
    :param data: formatted data
    """

    logger.debug("Saving file %s", filename)

    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DEBUG_LEVEL = int(ARGS.debug)
    set_log_level(DEBUG_LEVEL)

    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)




"""
Lesson 09 Assignment - Part 1
Decorators
"""

import argparse
import json
import datetime
import math
import logging

LOGGER = logging.getLogger(__name__)


def parse_cmd_arguments():
    """
    Parses arguments from the command line.
    :return: Values for input file, output file, debug level, conditional logging.
    """
    parser = argparse.ArgumentParser(description='Process input from the command line.')
    parser.add_argument('-i', '--input', help='Input JSON file', required=True)
    parser.add_argument('-o', '--output', help='Output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='Set debug level. 0=Off, 1=Error, 2=Warning, 3=Debug',
                        required=False, default=0)
    parser.add_argument("-c", "--conditional", help="Set conditional logging. 0=Off, 1=On",
                        required=False, default=0)

    return parser.parse_args()


def set_log_level(log_level):
    """
    Sets the log level for the debugger.
    :param log_level: 0, 1, 2, or 3
    """
    if log_level == 0:
        return

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler('charges_calc.log')
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)

    if log_level == 1:
        LOGGER.setLevel(logging.ERROR)
    elif log_level == 2:
        LOGGER.setLevel(logging.WARNING)
    elif log_level == 3:
        LOGGER.setLevel(logging.DEBUG)


def conditional_log(func):
    """
    Decorator for conditional logging.
    :param func: function
    :return: wrapper
    """
    def not_logged(*args, **kwargs):
        logging.disable(logging.CRITICAL)  # Turn logging off
        result = func(*args, **kwargs)  # Run function
        logging.disable(logging.NOTSET)  # Turn logging on
        return result
    return not_logged


def load_rentals_file(filename):
    """
    Loads rental data from the source file.
    :param filename: source file
    :return: data
    """
    LOGGER.debug("Opening file %s", filename)

    with open(filename) as file:
        try:
            data = json.load(file)
        except ValueError:
            logging.error("Error reading input file %s", file)
            exit(0)
    return data


@conditional_log
def calculate_additional_fields(data):
    """
    Calculates additional metrics.
    :param data: Data from the source file.
    :return: Additional metrics from the data.
    """
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as date_error:
            LOGGER.error("%s. Date format is incorrect.", date_error)
            LOGGER.debug(value)

        value['total_days'] = (rental_end - rental_start).days

        if value["total_days"] < 0:
            LOGGER.error("Total days is negative. Check rental start and end dates.")
            LOGGER.debug(value)

        value['total_price'] = value['total_days'] * value['price_per_day']

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError as math_error:
            LOGGER.warning("%s. Error with square root of total price.", math_error)
            LOGGER.debug(value)

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as zero_error:
            LOGGER.warning("%s. Error with units rented. Cannot divide by 0.", zero_error)
            LOGGER.debug(value)
    return data


def save_to_json(filename, data):
    """
    Saves the results to the output file.
    :param filename: output filename
    :param data: formatted data
    """
    LOGGER.debug("Saving file %s", filename)

    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DEBUG_LEVEL = int(ARGS.debug)
    set_log_level(DEBUG_LEVEL)

    DATA = load_rentals_file(ARGS.input)
    FINAL_DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, FINAL_DATA)

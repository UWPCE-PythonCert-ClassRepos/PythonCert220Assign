"""
Returns total price paid for individual rentals
"""

import argparse
import json
import datetime
import math
import logging

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOGGER = logging.getLogger()


def parse_cmd_arguments():
    """
    Parses arguments from command line
    :return:
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='enable debug logging', required=False, default=0)

    return parser.parse_args()


def set_log_level(log_level):
    """
    Sets log level for debugger
    :param log_level: 0, 1, 2, or 3
    :return:
    """

    if log_level == 0:
        return None

    file_handler = logging.FileHandler('charges_calc.log')

    file_handler.setFormatter(FORMATTER)

    LOGGER.addHandler(file_handler)

    if log_level == 1:
        LOGGER.setLevel(logging.ERROR)
    elif log_level == 2:
        LOGGER.setLevel(logging.WARNING)
    elif log_level == 3:
        LOGGER.setLevel(logging.DEBUG)

    return LOGGER


def load_rentals_file(filename):
    """
    Load rental data from source file.
    :param filename: source file
    :return: data
    """

    logging.debug("Opening file %s", filename)
    with open(filename) as file:
        try:
            data = json.load(file)
        except ValueError as err:
            logging.error("Error reading input file %s", file)
            print(f"Error reading the input file: {err}")
            exit(0)
    return data


def calculate_additional_fields(data):
    """
    Calculates additional metrics.
    :param data: Data from source file.
    :return:
    """
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as date_error:
            logging.error("%s Date format is incorrect.", date_error)
            print(f"Date format is incorrect. Should be m/d/y.")
            logging.debug(value)

        value['total_days'] = (rental_end - rental_start).days

        if value["total_days"] < 0:
            logging.error("Total days is negative.")
            print("Total days cannot be negative. Check rental start and end dates.")
            logging.debug(value)

        value['total_price'] = value['total_days'] * value['price_per_day']

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError as math_error:
            logging.warning("%s - Error with square root of total price.", math_error)
            print("Error with square root of total price.")
            logging.debug(value)

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as zero_error:
            logging.warning("%s Cannot divide by 0.", zero_error)
            print("Error with units rented. Cannot divide by 0.")
            logging.debug(value)
    return data


def save_to_json(filename, data):
    """
    Saves results to output file
    :param filename: output filename
    :param data: formatted data
    :return:
    """

    logging.debug("Saving file %s", filename)

    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DEBUG_LEVEL = int(ARGS.debug)
    set_log_level(DEBUG_LEVEL)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)

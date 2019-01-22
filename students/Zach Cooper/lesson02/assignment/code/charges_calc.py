"""
Returns total price paid for individual rentals
"""

import argparse
import json
import datetime
import math
import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
logger = logging.getLogger()


def parse_cmd_arguments():
    """
    Parses commands from the commandline
    """
    debug_logging_level_help = 'debug logging level \n\
                        0: No debug messages or log file.\n\
                        1: Only error messages.'

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument(
        '-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument(
        '-d', '--debug', help=debug_logging_level_help, required=False, default=0)
    return parser.parse_args()


def configure_logging_level(log_level):
    """
    Configures the logging

    Sets different log levels for debugger
    :paramater log_levels: 1(Error), 2(Debug), 3(Warning)
    :return:
    """
    # Breakdown of what will be returned under each level
    if log_level == 0:
        return None

    file_handler = logging.FileHandler('charges_calc_log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if log_level == 1:
        logger.setLevel(logging.ERROR)
    elif log_level == 2:
        logger.setLevel(logging.WARNING)
    elif log_level == 3:
        logger.setLevel(logging.DEBUG)

    return logger

    # # Could also put levels in a dict
    # log_level = {'0': logging.CRITICAL,
    #               '1': logging.ERROR,
    #               '2': logging.WARNING,
    #               '3': logging.DEBUG}


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
        except Exception as err:
            logging.error("Error reading input file %s", file)
            print(f"Error reading the input file: {err}")

    return data


def calculate_additional_fields(data):
    """
    Calculates additional metrics.
    # How to deal with Nulls for datetime?
    :param data: Data from source file.
    :return:
    """
    # Date Field
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as date_error:
            logging.error("%s The date format is incorrect.", date_error)
            print(f"Date format is not correct. Should be m/d/y.")
            logging.debug(value)

        # Total Days Field
        value['total_days'] = (rental_end - rental_start).days
        if value["total_days"] < 0:
            logging.error("Total days is negative: %s", value)
            print("Total days should not be negative. Rental start and rental end"
                  "dates need to be checked.")
            logging.debug(value)

        # Total Price Field
        value['total_price'] = value['total_days'] * value['price_per_day']
        try:

            # Total Square Price Field
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError as math_error:
            logging.warning("%s - Error with square root of total price.", math_error)
            print("Error with square root of total price.")
            logging.debug(value)
        try:

            # Unit Cost Field
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as zero_error:
            logging.warning("%s Cannot divide by 0.", zero_error)
            print("Error with units rented raised. You can't divide by 0.")
            logging.debug(value)
    return data


def save_to_json(filename, data):
    """
    Saves results to output file as new JSON
    :param filename: output filename
    :param data: formatted data
    :return:
    """
    logging.debug("save_to_json")
    logging.debug("Writes updated json file as outfile")
    with open(filename, 'w') as file:
        if data is None:
            logging.warning("No data is outputed")
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    debug_level = int(ARGS.debug)
    configure_logging_level(debug_level)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)

'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
#import os

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

FORMATTER = logging.Formatter(LOG_FORMAT)

LOGGER = logging.getLogger(__name__)


def turn_off_logging(func):
    """
    Decorator to turn off logging
    """

    def decorated_func(*args, **kwargs):
        logging.disable(logging.CRITICAL)
        print("something_else")
        returned_value = func(*args, **kwargs)
        logging.disable(logging.NOTSET)
        print("something")
        return returned_value

    return decorated_func


def parse_cmd_arguments():
    """
    function runs program from the command line
f
    args: input data file and output file name are required, logging is optional
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='enable debug logging', required=False)

    return parser.parse_args()


# def check_output_directory(filename):
#     if not os.path.exists(filename):
#         os.makedirs()


def set_log_level(log_level=0):
    """
    function to set level of logging desired from command line when running program
    :param log_level: 0, 1, 2, or 3
    :return: returns different level of logging when running the program
    """
    if log_level == 0:
        return
    file_handler = logging.FileHandler('my_log.log')
    file_handler.setFormatter(FORMATTER)
    LOGGER.addHandler(file_handler)
    if log_level == 1:
        LOGGER.setLevel("ERROR")
    if log_level == 2:
        LOGGER.setLevel("WARNING")
    if log_level == 3:
        LOGGER.setLevel("DEBUG")


def load_rentals_file(filename):
    """
    function to load input file, exits if issues are found with the input file
    :param filename: name of JSON file to be evaluated by program
    :return: data in file
    """
    LOGGER.debug("opening file in JSON " + str(filename))
    with open(filename) as file:
        try:
            data = json.load(file)
        except Exception as err:
            LOGGER.error(err)
            print(f"Something went wrong with the input file, {err}")
            exit(0)
    return data


@turn_off_logging
def calculate_additional_fields(data):
    """
    function to calculate days an item is rented, how long it was rented, how much it cost
    to rent for that time
    :param data: pulls data from input JSON file opened in load_rentals_file()
    :return: calculated values of days an item is rented, how long it was rented,
    how much it cost to rent for that time
    """
    for value in data.values():
        LOGGER.debug(value)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as date_error:
            LOGGER.error(date_error)
            print(f"Date is in incorrect format. Should match m/d/y.")
        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            LOGGER.error(f"Negative Total Days: {value}")
            #this line will exit the program
            # raise ValueError(f"Total days cannot be negative. Please check dates. "
            #                  f"Problem with {value}")
        value['total_price'] = value['total_days'] * value['price_per_day']
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError as math_error:
            LOGGER.warning("math problem %s %s", math_error, value)
            value['sqrt_total_price'] = None
            # print(f"Look at your input file, dummy. {math_error}")
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as zero_error:
            LOGGER.warning(zero_error, value)
            value['unit_cost'] = 0

    return data


def save_to_json(filename, data):
    """
    function to save calculated values from calculate_additional_fields() into an output JSON file,
    name specified in parse_cmd_arguments()
    :param filename: name specified in parse_cmd_arguments()
    :param data: calculated values from calculate_additional_fields()
    :return: calculated values from calculate_additional_fields() in JSON file
    """
    LOGGER.debug(filename)
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    # import pdb; pdb.set_trace()
    set_log_level(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)

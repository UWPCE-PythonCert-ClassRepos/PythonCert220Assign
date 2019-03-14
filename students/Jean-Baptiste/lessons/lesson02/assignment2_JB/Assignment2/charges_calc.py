"""
 This is calculate the output with json Returns total price paid for individual rentals
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
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='enable debug logging', required=False)
    return parser.parse_args()

def set_log_level(log_level=0):
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
    logging.debug("opening file in JSON " + str(filename))
    with open(filename) as file:
        try:
            data = json.load(file)
        except Exception as err:
            logging.error(err)
            print(f"Something went wrong with the input file, {err}")
            exit(0)
    return data


def calculate_additional_fields(data):
    for value in data.values():
        logging.debug(value)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as date_error:
            logging.error(date_error)
            print(f"Date is in incorrect format. Should match m/d/y.")
        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.error(f"Negative Total Days: {value}")
            raise ValueError(f"Total days cannot be negative. Please check dates. "
                              f"Problem with {value}")
        value['total_price'] = value['total_days'] * value['price_per_day']
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError as math_error:
            logging.warning("math problem %s %s", math_error, value)
            value['sqrt_total_price'] = None
            print(f"Look at your input file, dummy. {math_error}")
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as zero_error:
            logging.warning(zero_error, value)
            value['unit_cost'] = 0

    return data


def save_to_json(filename, data):
    logging.debug(filename)
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    set_log_level(str(ARGS.debug))
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)

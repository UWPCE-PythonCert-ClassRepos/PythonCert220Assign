'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging
import sys


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=False, default=0)
    return parser.parse_args()


def load_rentals_file(filename):
    logging.debug(f'Attempting to load JSON file {filename}')

    with open(filename) as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            logging.error(f'JSON file ({filename}) is improperly formatted.')
            exit(0)

    logging.debug(f'JSON file {filename} loaded successfully')
    return data

def calculate_additional_fields(data):
    for value in data.values():
        logging.debug(f'Reading values for {value}')

        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.error(f'Experienced a ValueError on {value}. Fix your data.')
            sys.exit()

        value['total_days'] = (rental_end - rental_start).days
        value['total_price'] = value['total_days'] * value['price_per_day']

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.error('Issue calculating total price. Fix your data.')
            sys.exit()

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.error('Unable to calculate cost, check values of price and units_rented. Fix your data.')
            sys.exit()

        logging.debug(f'Completed processing: {value}')
    return data


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)


def set_logging(level):
    log_format = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s')
    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_format)
    logger = logging.getLogger()
    logger.addHandler(file_handler)

    # 0: No debug messages or log file.
    # 1: Only error messages.
    # 2: Error messages and warnings.
    # 3: Error messages, warnings and debug messages.
    if level == 0:
        return

    if level == 1:
        logger.setLevel("ERROR")
        logger.debug(logging.ERROR)
    if level == 2:
        logger.debug("Logging mode set to WARNING")
        logger.setLevel(logging.WARNING)
    if level == 3:
        logger.debug("Logging mode set to DEBUG")
        logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    set_logging(int(args.debug))
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)

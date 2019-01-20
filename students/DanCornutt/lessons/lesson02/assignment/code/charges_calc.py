'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

log_format = ("%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
    %(message)s")
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler('changes_calc.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def parse_cmd_arguments():
    """Arguments for CLI"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    subparsers = parser.add_subparsers()
    parser.add_argument(
        '-i', '--input', help='input JSON file', required=True)
    parser.add_argument(
        '-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument(
        '-d', '--debug', help='debug mode')

    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logger.error('No file "{}" available to load.'.format(filename))
            exit(0)
    return data


def calculate_additional_fields(data):
    for value in data.values():
        logger.debug("Calculating fields for {} item".format(
            value['product_code']))
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
            if value['rental_end'] == "":
                logger.warning('rental_end is null')
                rental_end = datetime.datetime.now()
            else:
                rental_end = datetime.datetime.strptime(value['rental_end'],
                                                        '%m/%d/%y')
            value['total_days'] = abs((rental_end - rental_start).days)
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(abs(value['total_price']))
            if value['units_rented'] < 1:
                logger.warning('units rented less than 1')
                value['unit_cost'] = value['total_price']
                logger.error("Math failre. Setting unit cost equal to total \
                    price.")
            else:
                value['unit_cost'] = \
                    value['total_price'] / value['units_rented']
        except:
            exit(0)

    return data


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    # log_debug_setup('changes_calc.log', args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)

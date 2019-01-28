'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging


def log_debug_setup(debug_lvl):
    """Function sets up logging and debugging for script.
    param1: debug level 0 to 3"""
    log_format = ("%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
    %(message)s")
    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler('changes_calc.log')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if debug_lvl == "0":
        logger.disabled = True
    elif debug_lvl == "1":
        file_handler.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
    elif debug_lvl == "2":
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
    elif debug_lvl == "3":
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)

    return logger


def parse_cmd_arguments():
    """Argument parser for CLI"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        '-i', '--input', help='input JSON file', required=True)
    parser.add_argument(
        '-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument(
        '-d', '--debug', help='debug mode', choices=['0', '1', '2', '3'])

    return parser.parse_args()


def load_rentals_file(filename):
    """Opens file file, returns data
    prama1: json filename in local dir"""
    with open(filename) as file:
        try:
            data = json.load(file)
        except (json.decoder.JSONDecodeError):
            logs.error("Error loading json. Exiting program.")
            exit(0)
    return data


def calculate_additional_fields(data):
    """From data in memory, calculates needed fields for transaction
    param1: customer transaction data"""
    for value in data.values():
        logs.debug("Calculating fields for {} item".format(
            value['product_code']))
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
            if value['rental_end'] == "":
                logs.warning('rental_end is null')
                logs.error('setting rental_end date to now')
                rental_end = datetime.datetime.now()
            else:
                rental_end = datetime.datetime.strptime(value['rental_end'],
                                                        '%m/%d/%y')
            value['total_days'] = abs((rental_end - rental_start).days)
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(abs(value['total_price']))
            if value['units_rented'] < 1:
                logs.warning('units rented less than 1')
                value['unit_cost'] = value['total_price']
                logs.error("Math failure. Setting unit cost equal to total \
                    price.")
            else:
                value['unit_cost'] = (value['total_price'] /
                                      value['units_rented'])
        except ValueError:
            logs.error("Value error in data, continuing...")
            continue

    return data


def save_to_json(filename, data):
    """Saves data in memory to json file in current working dir
    param1: filename of to be saved data
    param2: data in memory"""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    logs = log_debug_setup(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)

'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math

import logging
import traceback, sys


log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
# BEGIN NEW STUFF
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler('mylog.log')
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)
# END NEW STUFF

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            logging.error("Error loading json from file {}".format(filename))
            logging.exception("message")
            exit(1)
    return data

def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            if value['units_rented'] == 0:
                value['unit_cost'] = value['total_price']
            else:
                value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            logging.error("Error calculating input data")
            logging.exception("message")
            exit(1)

    return data

def save_to_json(filename, data):
    """ To get utf8-encoded file as opposed to ascii-encoded,
      json.dump writes to a text file, it's output is ASCII-only by default,
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4,ensure_ascii=False)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)

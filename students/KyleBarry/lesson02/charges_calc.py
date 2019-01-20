'''
Returns total price paid for individual rentals
'''
import logging
import argparse
import json
import datetime
import math

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+".log"

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, filename=LOG_FILE)


def parse_cmd_arguments():
    """Accepts arguments for input and output from command line"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    """Attempt to load json data, print error message if failure"""
    with open(filename) as file:
        try:
            data = json.load(file)
            # logging.info("JSON has successfully loaded")
        except Exception:
            print("Your json file could not load, check syntax""")
            logging.ERROR("JSON file couldn't load")
            exit(0)
    return data


def calculate_additional_fields(data):
    """Add new values to data"""
    for value in data.values():
        try:
            try:
                rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            except ValueError:
                print(f"Time data is in incorrect format for {value['product_code']}")
            # logging.debug(rental_start)
            # logging.debug(rental_end)
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 0:
                value['total_days'] = abs(rental_end - rental_start).days
                print(f"Your start date is after your end date for {value['product_code']}")
                print("We assumed you flipped the dates and returned the difference.")
            # logging.debug(value['total_days'])
            value['total_price'] = value['total_days'] * value['price_per_day']
            # if value['total_days'] < 0:
            #     logging.warning("total_days is negative")
            # if value['price_per_day'] < 0:
            #     logging.warning("price_per_day  is negative")
            # if value['total_price'] < 0:
            #     logging.warning('total_price value is negative')
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            # logging.debug(values['sqrt_total_price'])
            # logging.debug(value['sqrt_total_price'])
            if value['units_rented'] == 0:
                print(f"Your units_rented is equal to zero for {value['product_code']}")
                # logging.warning("units_rented is equal to 0 and will throw an error")
            else:
                value['unit_cost'] = value['total_price'] / value['units_rented']
            # logging.debug(value['unit_cost'])
            # logging.debug(value['total_days'])
            # logging.debug(value['total_price'])
            # logging.debug(value['sqrt_total_price'])
            # logging.debug(value['unit_cost'])
        except Exception as e:
            logging.error(e)
            print(f"An unexpected error occurred: {e}")
            exit(0)

    return data


def save_to_json(filename, data):
    """Save new data to new json file"""
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)

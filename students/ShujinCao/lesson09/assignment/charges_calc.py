'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging


def main():
    """
    main function
    """
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    args = parse_cmd_arguments()
    if args.debug == 1:
        logging.basicConfig(level=logging.ERROR, format=log_format,
                            filename=log_file, filemode="a+")
    if args.debug == 2:
        logging.basicConfig(level=logging.WARNING, format=log_format,
                            filename=log_file, filemode="a+")
    if args.debug == 3:
        logging.basicConfig(level=logging.DEBUG, format=log_format,
                            filename=log_file, filemode="a+")
    input_data = load_rentals_file(args.input)
    logging.warning("DATA READ IN DONE - CALCULATION START")
    output_data = calculate_additional_fields(input_data)
    logging.warning("CALCULATION DONE - SAVE OUTPUT TO JSON FILE")
    save_to_json(args.output, output_data)
    logging.warning("OUTPUT HAS BEEN SUCCESFULLY SAVED")

def parse_cmd_arguments():
    """
    add arguments
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument(
        '-o',
        '--output',
        help='ouput JSON file',
        required=True)
    parser.add_argument(
        "-d",
        "--debug",
        type=int,
        choices=range(
            0,
            4),
        help="0: No debug messages or log file.\
                         1: Only error messages.\
                         2: Error messages and warnings.\
                         3: Error messages, warnings and debug messages")

    return parser.parse_args()


def load_rentals_file(filename):
    """
    load json file
    """
    with open(filename) as file:
        try:
            json_f = json.load(file)
        except BaseException:
            logging.error("DATA WAS NOT LOADED.")
            exit(0)
    return json_f

def turn_off_logging(func):

    def decorated_func(*args, **kwargs):
        logging.disable(logging.CRITICAL)
        print("some logging has been disabled")
        returned_value = func(*args, **kwargs)
        logging.disable(logging.NOTSET)
        print("some logging has been re-enabled")
        return returned_value

    return decorated_func

@turn_off_logging
def calculate_additional_fields(data):
    """
    calculations
    """
    for value in data.values():
        rental_start = datetime.datetime.strptime(
            value['rental_start'], '%m/%d/%y')
        try:
            rental_end = datetime.datetime.strptime(
                value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.error("CALCULATION ERROR FOR RENTAL_END")
            logging.warning(
                "QUICK FIX : REPLACING RENTAL_END WITH RENTAL_START")
            rental_end = datetime.datetime.strptime(
                value['rental_start'], '%m/%d/%y')
        logging.debug("rental_start : %s; rental_end : %s", rental_start, rental_end)
        value['total_days'] = (rental_end - rental_start).days
        value['total_price'] = abs(
            value['total_days'] *
            value['price_per_day'])
        value['sqrt_total_price'] = math.sqrt(value['total_price'])
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.error(
                "Tried to divide by zero; QUICK FIX: SET UNIT_COST TO ZERO")
            value['unit_cost'] = 0
        logging.debug("total_days: %s, total_price: %s, sqrt_total_price\
                      : %s, unit_cost: %s",
                      value['total_days'], value['total_price'], \
                      value['sqrt_total_price'], value['unit_cost'])
    return data


def save_to_json(filename, data):
    """
    save to json file
    """
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()

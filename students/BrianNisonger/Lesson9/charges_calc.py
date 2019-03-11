'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging


def turn_off_logging(func):
    """
    Decorator to turn off logging
    """

    def decorated_func(*args, **kwargs):
        if logging_dict["level"] == "1":
            logging.getLogger().disabled = True
        returned_value = func(*args, **kwargs)
        if logging_dict["level"] == "1":
            logging.getLogger().disabled = False
        return returned_value

    return decorated_func


def parse_cmd_arguments():
    """
    Parses commands from the commandline
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument(
        '-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument(
        '-d', '--debug', help='debugger level', required=False, default=0)
    parser.add_argument(
        '-l', '--logging', help='turn off logging', required=False, default=0)
    return parser.parse_args()


def configure_logging(debug_level):
    """
    Configures the logging
    """
    format_logger = '%(asctime)s %(filename)s:%(lineno)-3d%(levelname)s'
    format_logger += ' %(message)s'
    log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
    debug_level = int(debug_level)
    if debug_level == 0:
        logging.basicConfig(level=logging.CRITICAL)
    if debug_level > 0:
        logging.basicConfig(format=format_logger, level=logging.ERROR)
        f_handler = logging.FileHandler(log_file)
        f_handler.setLevel(logging.WARNING)
        logging.getLogger().addHandler(f_handler)
    if debug_level == 2:
        logging.getLogger().setLevel(logging.WARNING)
    if debug_level == 3:
        logging.getLogger().setLevel(logging.DEBUG)


@turn_off_logging
def load_rentals_file(filename):
    """
    Loads json file of rental data
    """
    logging.debug("load_rentals_file")
    logging.debug("Opens a json file and reads it in")
    with open(filename) as file:
        try:
            data1 = json.load(file)
        except Exception as error_msg:
            logging.error(error_msg)
            data1 = None
    return data1


@turn_off_logging
def calculate_additional_fields(data_new):
    """
    Calculates additional fields from raw property data
    """
    logging.debug("calculate_additional_fields")
    if data_new:
        for value in data_new.values():
            try:
                warning_string = f"Incorrect date for {value['product_code']}"
                if value["rental_start"] == '' or value["rental_end"] == '':
                    rental_start = 0
                    rental_end = rental_start
                    logging.warning(warning_string)
                    logging.debug(value)
                else:
                    rental_start = datetime.datetime.strptime(
                        value['rental_start'], '%m/%d/%y')
                    rental_end = datetime.datetime.strptime(
                        value['rental_end'], '%m/%d/%y')
                if rental_start >= rental_end:
                    value['total_days'] = 0
                    logging.warning(warning_string)
                    logging.debug(value)
                else:
                    value['total_days'] = (rental_end - rental_start).days
                value['total_price'] = value['total_days'] * value[
                    'price_per_day']
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
                if value["total_price"] == 0:
                    value["unit_cost"] = 0
                    warning_price = "Incorrect price for "
                    warning_price += f"{value['product_code']}"
                    logging.warning(warning_price)
                    logging.debug(value)
                else:
                    value['unit_cost'] = value['total_price'] / value[
                        'units_rented']
            except Exception as error_msg:
                logging.error(error_msg)
                logging.debug(value)
                data_new = None
                break
    else:
        logging.warning("No Data loaded from file")
    return data_new


def save_to_json(filename, data_out):
    """
    Writes property data to JSON file
    """
    logging.debug("save_to_json")
    logging.debug("Writes out updated json file")
    with open(filename, 'w') as file:
        if data_out is None:
            logging.warning("No Data will be written to file")
        json.dump(data_out, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    logging_dict = {}
    logging_dict["level"] = ARGS.logging
    configure_logging(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)

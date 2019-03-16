'''
Returns total price paid for individual rentals

This module reads a JSON file and expects each section to have 
product_coderental_start, rental_end, price_per_day and units_rented elements.
'''
import argparse
import json
import datetime
import math
import logging


def disable_method_logging(func):
    '''
    Decorator for disabling logging for specific methods
    :param func: decorator function argument
    '''
    def logging_disabled(*args, **kwargs):
        ''' Inner decorator function for disabling, running method and reenabling method '''
        logging.getLogger().disabled = True
        result = func(*args, **kwargs)
        logging.getLogger().disabled = False
        return result
    return logging_disabled


def load_logging(log_level, logger=None):
    '''
    Loads standard logging setup

    :param log_level: logging level from the user
    (1: Error, 2: Warning, 3: Debug)
    '''
    log = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    debug_dict = {'1': logging.ERROR, '2': logging.WARNING, '3': logging.DEBUG}    

    if log_level in debug_dict: 
        if logger is None:
            logger = logging.getLogger()
        logger.setLevel(debug_dict.get(log_level, logging.CRITICAL))

        file_name = f'{datetime.datetime.now().strftime("%Y-%m-%d")}.log'
        formatter = logging.Formatter(log)

        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)        
            
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

def load_rentals_file(filename):
    '''
    Loads the source JSON file

    :param filename: file name to load
    '''

    result = None
    try:
        with open(filename) as file:
            try:
                result = json.load(file)
                logging.debug(f"File loaded successfully: {filename}")
            except json.decoder.JSONDecodeError as json_decode_error:
                print(f"Error occurred while reading the JSON file")
                logging.error(f"Error loading JSON: {filename}: " + \
                    f"{str(json_decode_error)}")

    except FileNotFoundError as file_not_found:
        print(f"Source file not found: {filename}")
        logging.error(
            f"Source file not found: {filename}: {str(file_not_found)}")

    return result

def calculate_additional_fields(input_data):
    '''
    Calculates additional field values based on source file values

    :param data: dictionary of source file values
    '''
    key_log = "Invalid data: {0}: missing {1} value: {2}"
    for key, value in input_data.items():
        try:
            rental_start = datetime.datetime.strptime(
                value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(
                value['rental_end'], '%m/%d/%y')            
        except KeyError as key_err:
            logging.warn(key_log.format(key, key_err.args[0], str(key_err)))
            print(f"WARNING: {key} missing {key_err.args[0]} value")
        except ValueError as value_error:
            logging.warn(f"Invalid data: {key}: {str(value_error)}")
            print(f"WARNING: {key} has an invalid rental date value")

        value['total_days'] = (rental_end - rental_start).days

        if value['total_days'] < 0:
            logging.error(f"Invalid data: {key} rental start " + \
                f"{rental_start} is greater than the end {rental_end}")
            print(f"ERROR: {key} rental start is greater than end")

        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
        except KeyError as key_err:
            logging.warn(key_log.format(key, key_err.args[0], str(key_err)))
            print(f"WARNING: {key} missing {key_err.args[0]} value")
        except ValueError as value_error:
            logging.warn(f"Invalid data: {key}: {str(value_error)}")
            print(f"WARNING: {key} has invalid price_per_day")

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError as value_error:
            logging.warn(f"Invalid data: {key}: {str(value_error)}")
            print(
                f"WARNING: {key} unable square root the negative total_price")           
        
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except KeyError as key_err:
            logging.warn(key_log.format(key, key_err.args[0], str(key_err)))
            print(f"WARNING: {key} missing {key_err.args[0]} value")
        except ValueError as value_error:
            logging.warn(f"Invalid data: {key}: {str(value_error)}")
            print(f"WARNING: {key} has invalid units_rented value")
        except ZeroDivisionError as zero_error:
            logging.warn(
                f"Invalid data: {key}: units_rented is 0: {str(zero_error)}")
            print(f"WARNING: {key} units_rented cannot be 0")

def save_to_json(filename, file_data):
    '''
    Outputs the results to the JSON ouput file

    :param filename: output file name
    :param data: data to write to file
    '''
    with open(filename, 'w') as file:
        json.dump(file_data, file, indent=4)
        logging.debug(f"Output file generated: {filename}")
        print("Output file complete")

def parse_cmd_arguments():
    ''' Processes commandline arguments from the user '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='ouput JSON file', required=False)

    parser.add_argument('-l', '--log_off', help='ouput JSON file', required=False)

    result_args = parser.parse_args()
    load_logging(result_args.debug)

    logging.debug(f"Input: {result_args.input}")
    logging.debug(f"Output: {result_args.output}")
    logging.debug(f"Debug: {result_args.debug}")
    logging.debug(f"log_off: {result_args.log_off}")

    return result_args

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()

    # Selective method logging deactivate
    if ARGS.log_off is not None:
        if 'load' in ARGS.log_off.lower():
            load_rentals_file = disable_method_logging(load_rentals_file)
        if 'calc' in ARGS.log_off.lower():
            calculate_additional_fields = disable_method_logging(calculate_additional_fields)
        if 'save' in ARGS.log_off.lower():
            save_to_json = disable_method_logging(save_to_json)

    DATA = load_rentals_file(ARGS.input)
    if DATA is None:
        exit(0)
    calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)

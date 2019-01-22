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



def load_logging(log_level, logger=None):
    '''
    Loads standard logging setup

    :param log_level: logging level from the user
    (1: Error, 2: Warning, 3: Debug)
    '''
    log = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    debug_dict = {'1': logging.ERROR, '2': logging.WARNING, '3': logging.DEBUG}
    if logger is None:
        logger = logging.getLogger()
    logger.setLevel(debug_dict.get(log_level, logging.CRITICAL))

    if log_level in debug_dict:        
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

def parse_cmd_arguments():
    ''' Processes commandline arguments from the user '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='ouput JSON file', required=False)

    result_args = parser.parse_args()
    load_logging(result_args.debug)

    logging.debug(f"Input: {result_args.input}")
    logging.debug(f"Output: {result_args.output}")
    logging.debug(f"Debug: {result_args.debug}")

    return result_args


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

    for key, value in input_data.items():
        try:
            rental_start = datetime.datetime.strptime(
                value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(
                value['rental_end'], '%m/%d/%y')            

            value['total_days'] = (rental_end - rental_start).days

            if value['total_days'] < 0:
                logging.error(f"Invalid data: {key} rental start " + \
                    f"{rental_start} is greater than the end {rental_end}")
                print(f"ERROR: {key} rental start is greater than end")
                continue

            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except KeyError as key_error:
            logging.warning(f"Invalid data: {key}: missing " + \
                f"{key_error.args[0]} value: {str(key_error)}")
            print(f"WARNING: {key} missing {key_error.args[0]} value")
        except ValueError as value_error:
            logging.warning(f"Invalid data: {key}: {str(value_error)}")
            print(f"WARNING: {key} has invalid data values")
        except ZeroDivisionError as zero_error:
            logging.warning(f"Invalid data: {key}: units_rented is 0: {str(zero_error)}")
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

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.input)
    if DATA is None:
        exit(0)
    calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)

#Tim Pauley
#Assignment 02
#Date: Jan 15 2019
'''
Requirements:

Your script needs to deal with data inconsistencies that could make it crash or return incorrect data (handle the exception and issue an error message for these and let the script continue) and issue warnings for missing data.

Capture you debug work in a text file called charges_calc.log. You will need that for your submission.

Setup logging messages so that they are disabled by default and can by enabled by using -d 1 or –debug 1 from the command line. Use the argparse module for this. You will have the following debug levels:
0: No debug messages or log file.
1: Only error messages.
2: Error messages and warnings.
3: Error messages, warnings and debug messages.
You need to implement three types of logging messages:
Debug: General comments, indicating where in the script flow we are. Should be shown on screen only (i.e., never saved to logfile).
Warning: Used for missing elements in the source data that force a change in the flow. Shown on screen and on the log file.
Error: Used for inconsistencies in the source data that will cause the script to crash or report incorrect results. Shown on screen and on the log file.
Use the following format for your log messages:

log_format = “%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s”

Use the following filename format to timestamp your log files:

log_file = datetime.datetime.now().strftime(“%Y-%m-%d”)+’.log’
'''

'''
Returns total price paid for individual rentals
'''

#pylint: disable=W0703

import logging
import argparse
import json
import datetime
import math



log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
logger = logging.getLogger()


def parse_cmd_arguments():
    """
    Parses commands from the commandline
    """
    debug_logging_level_help = 'debug logging level \n\
                        0: No debug messages or log file.\n\
                        1: Only error messages.'

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument(
        '-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument(
        '-d', '--debug', help=debug_logging_level_help, required=False, default=0)
    return parser.parse_args()


def confgure_logging(debug_lever):
    """"
    configures the logging
    """
    format_logger = '%(asctime)s %(filename)s:%(lineno)-3d%(levelname)s'
    format_logger += ' %(message)s'
    log_file = datetime.datetime.now().strptime('%Y-%m-%d') + '.log'
    debug_leve = int(debug_level)
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

def load_rentals_file(filename):
    """
    Loads the json file of rental data
    """
    logging.debug("load_rentals_file")
    logging.debug("Opens json file and readz it in")
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            logging.error(error_msg)
            logging.debug(i)
    return data

def calculate_additional_fields(data):
    """
    Calculates additional properties
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

def save_to_json(filename, data):
    """
    Writes property data to JSON file
    """
    logging.debug("Saving file %s", filename)
    with open(filename, 'w') as file:
        json.dump(data, file)    

if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)

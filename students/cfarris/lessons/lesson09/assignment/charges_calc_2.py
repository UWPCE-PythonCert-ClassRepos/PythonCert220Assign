#!/usr/bin/env Python3

'''
Lesson9 part2--edit file to use a decorator to toggle debugging on/off
from command line
Note: This script could use some linting. However, in the interest of time,
I am turning in as is. I would also like to add tests later on...during break
I apologize for the code smells!
'''

import functools
import argparse
import json
import datetime
import math
import logging



log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter = logging.Formatter(log_format)  #create a formatter

logger = logging.getLogger()  #calls the logger object


def parse_cmd_arguments():
    '''
    This function accepts parameters from user input and stores arguments until called
    #-d should turn debugging on or off. -d True turns dbug on, -d off turns debug off.
    #debug will be set to off
    PARAMS: input and output are required by user, debug level is optional
    RETURN: arguments provided by user
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='report logging debug', required=False)
    logging.debug(parser.parse_args())
    return parser.parse_args()



def set_logger(fn):
    '''
    set_logger is used a a decorator to turn logging on and off. 
    Logger is decorated and the debug argument is added from command line.
    '''
    def _decorator(debug, *args, **kwargs):
        if debug == 'False':
            result = fn(debug, *args)
            return result
        else:
            file_handler = logging.FileHandler('charges_calc.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.setLevel("INFO")
            result = fn(debug, *args)
            return result
    return _decorator


@set_logger
def load_rentals_file(debug, filename): 
    '''
    Loads a rental JSON file and will throw an error if it has trouble doing so.
    I put a generic error here as it could error due to file not found, or problems
    with the file itself.
    '''
    logging.debug('Opening provided JSON file... ' + filename)
    with open(filename) as file:
        try:
            data = json.load(file)  
        except Error as er_or:
             logging.error("An error occurred", er_or)
             print(f'Error with {filename}!')
             exit(0)
    return debug, data


@set_logger
def calculate_additional_fields(debug, data):
    '''
    Processes data contained in input file. Calculates 'total_days',
    'total_price','unit_cost', 'sqrt_total_price'
    PARAMS: input file (json file)
    RETURNS: data with new calculations
    '''
    print('debug passed to calculate_additional_fields', debug)
    for value in data[1].values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError as err:
            logging.error(err)
            print('Error with rental_start', value['rental_start'])

        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as err:
            logging.error(err)
            print('error with rental_end', value['rental_end'])

        try:
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] <= 0:
                logging.debug(f'rental_start and rental_end may have been entered backward.\
                                start:{rental_start} end:{rental_end}')
                value['total_days'] = (rental_start - rental_end).days
        except ValueError as err_or:
            logging.error("Error with value['total_days']!", err_or)

        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as err_or:
            total_price = value['total_price']
            units_rented = value['units_rented']
            logging.error(f'Units_rented must be greater than 0: {err_or} total_price:{total_price}, units_rented{units_rented}')
            print(f'An error occured calculating unit_cost: {err_or}. total_price:{total_price}, units_rented:{units_rented}')
            value['unit_cost'] = None
    return debug, data


@set_logger
def save_to_json(debug, filename, data):
    '''
    saves file with calculated values to disk
    PARAM: output file name, data
    RETURNS: output file in json format with data
    '''
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    debug = str(args.debug)
    data = load_rentals_file(debug, args.input)
    data = calculate_additional_fields(debug, data)
    save_to_json(debug, args.output, data)

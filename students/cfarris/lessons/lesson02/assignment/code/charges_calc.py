#!/usr/bin/env Python3

'''
Returns total price paid for individual rentals 
'''
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
    PARAMS: input and output are required by user, debug level is optional
    RETURN: arguments provided by user
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='report logging debug', required=False)
    logging.debug(parser.parse_args())
    return parser.parse_args()


def set_logging_preferences(debug='0'):
    '''
    sets logging preferences for debugging
    '''
    if debug == '0':
        print('debugging is off')
        return

    file_handler = logging.FileHandler('charges_calc.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if debug == '1':
        print('debug on, error only')
        logger.setLevel("ERROR")
    if debug == '2':
        print('error messages and warnings')
        logger.setLevel("WARNING")
    if debug == '3':
        print('error messages, warnings and debug messages')
        logger.setLevel("DEBUG")


def load_rentals_file(filename): 
    logging.debug('Error opening provided JSON file... ' + filename)
    with open(filename) as file:
        try:
            data = json.load(file) # good place to add an error file
        except Error as er_or:
             logging.error("An error occurred", er_or)
             print(f'Error with {filename}!')
             exit(0)
    return data

def calculate_additional_fields(data):
    '''
    Processes data contained in input file. Calculates 'total_days',
    'total_price','unit_cost', 'sqrt_total_price'
    PARAMS: input file (json file)
    RETURNS: data with new calculations
    '''
    for value in data.values():
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
    return data

def save_to_json(filename, data):
    '''
    saves file with calculated values to disk
    PARAM: output file name, data
    RETURNS: output file in json format with data
    '''
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    print(args.debug)
    set_logging_preferences(str(args.debug))
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)

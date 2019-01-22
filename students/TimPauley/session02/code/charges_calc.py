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

Assignment location: https://uwpce-pythoncert.github.io/PythonCertDevel220/modules/lesson02/assignment.html 

'''

'''
Returns total price paid for individual rentals 
'''
import logging
import argparse
import json
import datetime
import math

logging.basicConfig(level=logging.WARNING)
#add logging file path here

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    logging.debug(i)
    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0) #add catch statement here to catch the error
            logging.debug(i)
    return data

def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            exit(0)

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)

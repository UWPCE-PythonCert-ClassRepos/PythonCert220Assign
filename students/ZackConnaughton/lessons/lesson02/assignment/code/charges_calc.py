'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

def set_logging_level(level):
    """
    sets logging level based on level and creates a file to save the log to
    input: level as string
    return: None
    """

    level_dict = {'0': logging.CRITICAL,
                  '1': logging.ERROR,
                  '2': logging.WARNING,
                  '3': logging.DEBUG}

    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'

    formatter = logging.Formatter(log_format)
    logger = logging.getLogger()
    logger.setLevel(level_dict[level])

    if level == '0':
        return None

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level_dict[level])
    console_handler.setFormatter(formatter)

    log_file = datetime.datetime.now().strftime('0%Y-%m-%d') + '.log'

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return None

def parse_cmd_arguments():
    """
    arg parser function
    """
    debug_logging_help = 'debug logging level \n\
                        0: No debug messages or log file.\n\
                        1: Only error messages.\n\
                        2: Error messages and warnings.\n\
                        3: Error messages, warnings and debug messages.\n'
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help=debug_logging_help, default=0)

    return parser.parse_args()


def load_rentals_file(filename):
    """
    loads a file with furniture rental information
    input: filename as json file
    return: data as a dict
    """
    with open(filename) as file:
        try:
            data = json.load(file)
        except ImportError:
            logging.error("File not found: %s", repr(file))
            exit(0)
    return data

def calculate_additional_fields(data):
    """
    calculates statistical data for each record
    input: rental data dict
    return: data dict with additional fields
    """
    for index, value in data.items():
        try:
            logging.debug("Calculating additional values for %s",repr(index))
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            if value['rental_end'] == '':
                logging.warning("%s does not have a rental_end value. Used %s for \
                                rental_end", repr(index), repr(datetime.datetime.now()))
                rental_end = datetime.datetime.now()
            else:
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.error("Tried to square root a negative \
                          for {} with values{}".format(repr(index), repr(value)))
            continue
    return data

def save_to_json(filename, data):
    """
    save dict to JSON
    input: filename is the file, data as dict
    """
    logging.debug("Saving output to json file")
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    import pdb
    pdb.set_trace()
    set_logging_level(str(ARGS.debug))
    data = load_rentals_file(ARGS.input)
    data = calculate_additional_fields(data)
    save_to_json(ARGS.output, data)

'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

def logger_toggle(func):
    """ a timer decorator """
    if (ARGS.debug) == 0:
        # DO NOTHING
        return func

    else:
        def set_level(*args, **kwargs):
            """ nested function for timing functions """

            # start = time.time()
            value = func(*args, **kwargs)
            # end = time.time()
            # runtime = end - start
            # print(f' The runtime for {func.__name__} took {runtime} seconds to complete')
            return value
    return set_level


def parse_cmd_arguments():
    """
    Command line options
    """

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    #parser.add_argument('-l', '--logging', help='turn on logging', default='on')
    parser.add_argument('-d', '--debug', help='Debug Level', type=int, default = 0)
    return parser.parse_args()


def load_rentals_file(filename):
    """
    Open the specified json file
    """

    with open(filename) as file:
        logging.debug(f'Opening {filename}')
        try:
            data = json.load(file)
        except Exception as except_error:
            print(except_error)
            logging.error(except_error)
            exit(0)
    return data


def calculate_additional_fields(data):
    """
    Function that grabs the json data and creates addtional fields from the
    calculations of existing data; Total Days, Total Price, Square Root Total
     and Unit Cost
    """

    # for value in data.values():
    logging.debug("Looping thru the json file to calculate the additional fields!")
    for key, value in data.items():
        # grab the item and values
        logging.debug(f'Working with {key} {value}')
        # start calculating and creating the additional fields
        try:
            # a good place to check if the starting date is newer than the end
            # date and correct it if possible
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
        except Exception as except_error:
            logging.error(f': {key} : Error calculating Total Days: {except_error}')
            # pass
        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
            logging.debug(f"Updating {value} total price to: "
                            f"{value.get('total_price')}")
        except Exception as except_error:
            logging.error(f': {key} : Error calculating Total Price: {except_error}')
            # pass
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug(f"Updating {value} square root total price to: "
                           f"{value.get('sqrt_total_price')}")
        except Exception as except_error:
            logging.error(f": {key} : Error calculating the Square Root Total "
                            f"Price: {except_error}")
            # pass
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug(f"Updating {value} unit cost to: {value.get('unit_cost')}")
        except Exception as except_error:
            logging.error(f': {key} : Error calculating Unit Cost: {except_error}')
            # pass

    return data


def save_to_json(filename, data):
    """
    Save data to the output file
    """
    logging.debug(f"Saving to file {filename}")
    with open(filename, 'w') as file:
        json.dump(data, file)

def log_toggle(toggle):
    #the decorator func?
    if toggle == 'on':
        return(log_config(log_level=0))
    return(log_config(log_level=0))

# @logger_toggle
def log_config(log_level):
    """
    Configures the root logging parameters using the argument from argparse. Default
    is set to CRITICAL which effectively is no logging right now.
    """

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler('charges_calc.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.NOTSET)

    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if log_level == 1:
        logger.setLevel(logging.DEBUG)
        logging.info(f'Configuring logging parameters for DEBUG mode')

    elif log_level == 2:
        logger.setLevel(logging.WARNING)
        logging.info(f'Configuring logging parameters for WARNING mode')

    elif log_level == 3:
        logger.setLevel(logging.ERROR)
        logging.info(f'Configuring logging parameters for ERROR mode')

    else:
        logging.info(f'Going with default logging parameters which is NONE')



if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    logger_toggle(ARGS.debug)
    # enable_logging = log_toggle(ARGS.logging)
    # enable_logging(ARGS.debug)
    # # enable_logging(log_config, ARGS.debug)
    log_config(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)

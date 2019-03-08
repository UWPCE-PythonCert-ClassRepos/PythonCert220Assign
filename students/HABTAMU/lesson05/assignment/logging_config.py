# logging_config.py

import logging


# Create a custom logger for 'HP_Northon'
logger = logging.getLogger('HP_Northon')
logger.setLevel(logging.DEBUG)

# Create file handlers which logs even debug messages
f_handler = logging.FileHandler('mongodb.log')

# Create formatter and add it to handlers
f_format = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s')
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(f_format)

# Add handlers to the logger
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(f_format)
stream_handler.setLevel(logging.ERROR)
logger.addHandler(f_handler)
logger.addHandler(stream_handler)


from pathlib import Path
import os
import logging
import timeit
import time

logging.basicConfig(level=logging.ERROR)


def timerfunc(func):
    """ a timer decorator """

    def function_timer(*args, **kwargs):
        """ nested function for timing functions """

        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        print(f' The runtime for {func.__name__} took {runtime} seconds to complete')
        return value
    return function_timer

@timerfunc
def jpg_discovery(directory, png_paths=None):
    logging.info(f' directory is passed as: {directory}')
    if png_paths is None:
        png_paths = []
    for filename in os.listdir(directory):
        new_dir = os.path.join(directory, filename)
        # logging.info(f' new_dir value is {new_dir}')
        logging.info(f'looking at {directory} and {filename}')
        logging.info(f'is {filename} a directory?')
        logging.info(f'{os.path.isdir(os.path.join(directory, filename))}')
        # logging.info(f'{os.path.abspath(filename)}')
        if os.path.isdir(new_dir):
            logging.info(f' {filename} is a directory so passing back to function using {new_dir} as the filename')
            jpg_discovery(new_dir, png_paths)
            png_paths.append(str(new_dir))
        else:
            logging.info(f'checking the file extension on {filename} for PNG')
            if filename.endswith(".png"):
                logging.info(f'does {filename} end with png?')
                png_paths.append([filename])
    # print(png_paths)
    return png_paths

# sprint(jpg_discovery(os.getcwd()))
if __name__=="__main__":
    # import timeit
    # setup = "from __main__ import jpg_discovery"
    # print(timeit.timeit("jpg_discovery(os.getcwd)", setup=setup))
    jpg_discovery(os.getcwd())


# import pdb; pdb.set(trace()

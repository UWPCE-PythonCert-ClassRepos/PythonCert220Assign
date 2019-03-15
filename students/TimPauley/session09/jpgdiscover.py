#Tim Pauley
#Assingment 09
#Date: March 07 2019

#Assignment 09: decorators, context managers and recursion that can help to build 
#expressive programs that are easy to understand.


'''
Revisit your logging assignment from lesson 2. We are going to make 
logging selective, by using decorators.

Add decorator(s) to introduce conditional logging so that a single 
command line variable can turn logging on or off for decorated classes 
or functions.

Change the lesson 5 assignment to Write a context manager to access 
MongoDB. There is already an example in lesson 5, but build on this 
example. Try to add useful features based on your experience of the 
Python techniques you have learned.

HP Norton keeps pictures of all their furniture in jpg files that are 
stored on their file server. They have a very crude program that starts 
y discovering all directories on the server and then looking in each 
of those for the jpg files. They have discovered a problem, though: 
jpg files are not found when they are stored in directories that are 
more than one level deep from the root directory. Your job is to write 
a jpg discovery program in Python, using recursion, that works from a 
parent directory called images provided on the command line. The program
will take the parent directory as input. As output, it will return a 
list of lists structured like this: 
[“full/path/to/files”
, [“file1.jpg”
, “file2.jpg”,…]
, “another/path”
,[]
, etc] The program must be called jpgdiscover.py
'''

"""
Recursively go through directories looking for pngs
"""
from pathlib import Path
import os
import logging
import timeit
import time

logging.basicConfig(level=logging.ERROR)


def timerfunc(func):
    """ decorator function"""

    def function_timer(*args, **kwargs):
        """ this nested function for timing """

        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        print(f' runtime {func.__name__} timing {runtime} seconds to finish')
        return value
    return function_timer

@timerfunc
#this is the place where wI created a timer function
def jpg_discovery(directory, png_paths=None):
    logging.info(f' this passed: {directory}')
    if png_paths is None:
        png_paths = []
    for filename in os.listdir(directory):
        new_dir = os.path.join(directory, filename)
        # this is used for logging
        logging.info(f'looking at {directory} and {filename}')
        logging.info(f'is {filename} a directory')
        logging.info(f'{os.path.isdir(os.path.join(directory, filename))}')
        # this is for logging path
        if os.path.isdir(new_dir):
            logging.info(f' {filename} is a directory so passing back to function using {new_dir} as the filename')
            jpg_discovery(new_dir, png_paths)
            png_paths.append(str(new_dir))
        else:
        # this handles the exception	
            logging.info(f'checking the file extension on {filename} for PNG')
            if filename.endswith(".png"):
                logging.info(f'does {filename} end with png?')
                png_paths.append([filename])
    # printed output to see result
    return png_paths

# this is where the main method is located
if __name__=="__main__":
    jpg_discovery(os.getcwd())




#!/usr/bin/env Python3

'''
Lesson 09 discovery of png during walk down file tree
The file was supposed to be called jpgdiscover.py even though the 
sample directory we were given contained only pngs.

This code wasn't linted and is submitted as is...in the interest of time.
logging, linting and Tests will be added later during break.
'''

import os


##recursive example started in class
#use os.walk, but you can't do this with recursion.
#may also want to look up path
#https://docs.python.org/3/library/os.html

def jpg_discovery():
    '''
    Though specified in the assignment, the supplied directory tree only has .png files.
    It is therefore more pythonic to create a png_discovery.
    '''
    pass


def png_discovery(directory, png_paths=None):
    '''
    looks for png files  and returns the list of file paths. 
    '''
    if png_paths is None:
        png_paths = []
    directory_list = [ directory, [] ]
    for filename in os.listdir(directory):
        path_join = os.path.join(directory, filename)
        #if os.path.isdir(filename):
        #    png_paths.extend(png_discovery(filename, png_paths))
        if os.path.isdir(path_join):
            #png_paths.extend(png_discovery(path_join, png_paths))
            png_discovery(path_join, png_paths)
        if filename.endswith('.png'):
            directory_list[1].append(filename)
            png_paths.append(path_join)
    if directory_list[1]:
        png_paths.extend(directory_list)
    return png_paths


print(png_discovery(os.getcwd()))


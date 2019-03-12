#!/usr/bin/env python3

import os
import argparse


# 1 use decorator similar to class example, use argparse as well. logging.disabled = true
# 2 add context for connecting to mongoDB
# 3 Recursive function looks at files in local, returns .jpg via os.path, calls itself on all folders in local.

FILE_CONTENTS = []


def selective_log():
    """Item #1 from hw. Add decorators to introduce conditional logging. --In work
    """
    pass


def context_manager():  # 2
    """Lesson 5 already uses context manager for MongoDB connection.
    """
    pass


def jpeg_discovery(directory):
    """Item #3 from hw. Name is jpeg, looks for png files.
    Seems like a Windows program.
    param1: directory to begin search
    returns: list of lists for .png filepaths
    """
    jpegs = []
    for filename in os.listdir(directory):
        print(filename)
        if os.path.isdir(directory + "/" + filename):
            print("Yes is directory")
            jpeg_discovery(os.path.abspath(directory + "/" + filename))
        if filename.endswith(".png"):
            jpegs.append(filename)
    FILE_CONTENTS.append([os.path.abspath(directory + "/" + filename), jpegs])
    return FILE_CONTENTS


if __name__ == "__main__":
    search_tree = jpeg_discovery(os.getcwd() + '/data')
    print(search_tree)

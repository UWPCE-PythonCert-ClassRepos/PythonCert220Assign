# """ Recursively go through directories looking for pngs """
import functools
import sys
import csv
import os
import pathlib
import logging
import argparse
from pymongo import MongoClient

def png_discovery(directory, png_paths=None):
    if png_paths is None:
        png_paths = []
    current_list = [directory, []]
    for filename in os.listdir(directory):
        path_join = os.path.join(directory, filename)
        if os.path.isdir(path_join):
            png_discovery(path_join, png_paths)
        if filename.endswith(".png"):
            current_list[1].append(path_join)

    if current_list[1]:
        png_paths.extend(path_join)
        
    return current_list


if __name__ == '__main__':
    directory = os.getcwd()
    product_file = 'products.csv'
    customer_file = 'customers.csv'
    rental_file = 'rentals.csv'
    database_name = 'inventory'

    import_data(directory, product_file, customer_file,
                rental_file, connection=None, database_name=None)

    png_discovery(directory)

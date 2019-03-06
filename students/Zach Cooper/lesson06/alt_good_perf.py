#!/usr/bin/env pypy
"""
    Lesson06 Assignment

"""

from timeit import timeit
import datetime
import csv


def analyze(filename):
    """
        This function loops through the date strings and returns count for each year
        spanning 2012-2018. It then counts how many times 'ao' appears in the file. 
        This function does not convert the date string to datetime object but leaves 
        it as is because the file contains date all in the same format.
        :param: csv file
        :return: 
    """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # Skip the header rows so y
        next(reader, None)

        # Return year_count in a dictionary
        year_count = {}

        # Return 'ao' count start at 0
        found = 0

        # Loop through date strings between 2012 and 2018 and return count for each year
        # Date column is index 5 in file and [-4:] parseson just year of the date string
        for row in reader:
            if "2012" < row[5][-4:] < "2019":
                year_count[row[5][-4:]] = year_count.get(row[5][-4:], 0) + 1

        # Counts how many times 'ao' appears in file which
            if 'ao' in row[6]:
                found += 1

        print(year_count)
        print(f"'ao' was found {found} times")

        end = datetime.datetime.now()

    return start, end, year_count, found


def main():
    filename = "exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    print(timeit("analyze('exercise.csv')", globals=globals(), number=1))

#!/usr/bin/env Python3

"""
Revised module from poor_perf.py
Key modificationw was to count occurances of 'ao' during first read
Thereby obviating the need to open and close a large file twice.
Proof that this was the problem was shown by timeit, which cut runtime in half.
memory_profiler.profile was also run against poor_perf.py and good_perf.py
Memory consumption didn't appear to be a big issue. (from what I saw?)
While other improvements may be possible, I am stopping here to continue with
other assignments.
"""

import datetime
import csv
from timeit import timeit as timer
from memory_profiler import profile



#def analyze(filename): #correct one. need to figure out
@profile
def analyze():
    '''
    analyze opens up exercise.csv and counts the occurance of years 2013-2018
    and finds the number of occurances of 'ao' in a file. It returns the
    year count and number of 'ao'.
    '''
    filename = 'data/exercise.csv'
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        found = 0
        for row in reader:
            lrow = list(row)
            if "ao" in row[6]:
                found += 1
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for new in new_ones:
            if new[0][6:] == '2013':
                year_count["2013"] += 1
            if new[0][6:] == '2014':
                year_count["2014"] += 1
            if new[0][6:] == '2015':
                year_count["2015"] += 1
            if new[0][6:] == '2016':
                year_count["2016"] += 1
            if new[0][6:] == '2017':
                year_count["2017"] += 1
            if new[0][6:] == '2018':
                year_count["2017"] += 1
        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)


def main():
    '''
    Main runs the analyze function which at this
    time includes running timer and profiler
    on analyze. Analyze will return values,
    but the timer and profiler will return
    values about the programs performance.
    '''
    #filename = "data/exercise.csv" # timer kept choking when passed as parameter.
    print('\n\ntime to run analyze(filename)')
    print(timer('analyze()', globals=globals(), number=1))


if __name__ == "__main__":
    main()

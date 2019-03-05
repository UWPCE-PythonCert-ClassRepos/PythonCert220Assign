"""
poorly performing, poorly written module

"""

import datetime
import csv
import pandas as pd
import timeit

def analyze(filename):
    start = datetime.datetime.now()
    start_time = timeit.default_timer()
    df = pd.read_csv(filename)

    year_count = {'2013': 0,
                  '2014': 0,
                  '2015': 0,
                  '2016': 0,
                  '2017': 0,
                  '2018': 0}

    sub = df[" date"][df[" date"] > '00/00/2012']
    for i in sub.values:
        if "2013" in i:
            year_count["2013"] += 1
        elif "2014" in i:
            year_count["2014"] += 1
        elif "2015" in i:
            year_count["2015"] += 1
        elif "2016" in i:
            year_count["2016"] += 1
        elif "2017" in i:
            year_count["2017"] += 1
        elif "2018" in i:
            year_count["2018"] += 1

    print(year_count)

    found = df[" sentence"].str.contains("ao").sum()

    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()
    print(timeit.default_timer() - start_time)

    return (start, end, year_count, found)

def main():
    filename = "data/exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    main()

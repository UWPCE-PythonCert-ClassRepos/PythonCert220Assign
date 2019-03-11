"""
hw6 slightly better performing, slightly less poorly written module

"""

import datetime
import csv


def analyze(filename):
    start = datetime.datetime.now()
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)  # skips header

        new_ones = []
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }
        found = 0
        kw = "ao"

        for row in reader:
            yr_str = row[5]
            yr = yr_str[-4:]
            info = row[0]
            search_str = row[6]
            if kw in search_str:
                found += 1
            if yr >= '2012':
                new_ones.append((yr_str, info))
                try:
                    year_count[yr] += 1
                except KeyError:
                    continue

        print(year_count)
        print("'ao' was found {} times".format(found))

        end = datetime.datetime.now()

    return (start, end, year_count, found)


def main():
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()

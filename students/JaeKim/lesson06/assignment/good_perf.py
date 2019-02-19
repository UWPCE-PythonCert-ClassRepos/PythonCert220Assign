"""
poorly performing, poorly written module

"""

import datetime
import csv

def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        found = 0
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for row in reader:
            year = row[5][6:]

            if "ao" in row[6]:
                found += 1

            if year >= '2013':
                if year <= '2018:':
                    year_count[year] += 1

    end = datetime.datetime.now()

    print(year_count)
    print(f"'ao' was found {found} times")
    print(end - start)

    return start, end, year_count, found


def main():
    analyze("data/exercise.csv")


if __name__ == "__main__":
    main()

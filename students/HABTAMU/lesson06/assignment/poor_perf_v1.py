"""
poorly performing, poorly written module
"""

import datetime
import csv
from collections import defaultdict

def analyze(filename):
    start = datetime.datetime.now()
    year_count = defaultdict(lambda : 0)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        found = 0
        for row in reader:
            if (row[5][6:] > '2012') and (row[5][6:] < '2019'):
                year_count[row[5][6:]] += 1

            if "ao" in row[6]:
                found +=1

        print(f"'ao' was found {found} times")
        print(year_count)
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    filename = "lesson06_assignment_data_exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()

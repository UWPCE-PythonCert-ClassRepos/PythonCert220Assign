"""
poorly performing, poorly written module

"""

import time
import csv

def poor_analyze(filename):
    start = time.clock()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        for row in reader:
            lrow = list(row)
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
                year_count["2018"] += 1

        print(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1

        print(f"'ao' was found {found} times")
        end = time.clock()

    return (start, end, year_count, found)

def better_analyze(filename):
    start = time.clock()
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    found = 0
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            new_year = row[5][6:]
            if new_year in year_count:
                year_count[new_year] += 1
            if 'ao' in row[6]:
                found += 1
    print(year_count)
    print("'ao' was found %s times" % found)

    end = time.clock()

    return (start, end, year_count, found)

def main():
    filename = "data/exercise.csv"
    start, end, year_count, found = poor_analyze(filename)
    print("Poor performance at: %s" % (end - start))
    start, end, year_count, found = better_analyze(filename)
    print("Better performance at: %s" % (end-start))


if __name__ == "__main__":
    main()

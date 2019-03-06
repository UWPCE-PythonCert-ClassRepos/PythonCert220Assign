"""
from poorly to goodly performing, goodly written module
"""
import datetime
import csv
import collections
from datetime import datetime as dt

"""
Analyzes a file and produces a count of years and the number of times "ao" was found
"""
def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = (row[5] for row in reader)
        getter_of_years = (y[6:] for y in new_ones)
        year_count = collections.Counter(getter_of_years)
        filtered_year_dict = {year: year_count[year]
            for year in ["2013", "2014", "2015", "2016", "2017", "2018"]}
        print(filtered_year_dict)
        csvfile.seek(0)
        found = 0
        found_getter = (line[6] for line in reader)
        found = len([1 for x in found_getter if 'ao' in x])
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()
    return (start, end, filtered_year_dict, found)


def main():
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()



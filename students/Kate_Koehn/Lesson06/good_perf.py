"""
This module is the cleaned up version of poor_perf.py. The file is only read and iterated over a single time,
and all operations that need to be performed on each row have been consolidated into a single for loop.
"""
from timeit import timeit
import datetime
import csv


def analyze(filename):
    """
    Program to read in a csv, loop over the rows in the file, convert the date from a string to a datetime object,
    save count of years 2013-2018 in a dict, and count how many times "ao" appears in the file.
    """

    # timestamp for when we start executing the function
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        # skip header
        next(reader, None)
        # we only care about dates after 01/01/2012, this line converts that date to a datetime object to be able
        # to compare to other dates in the file
        date =  datetime.datetime.strptime('01/01/2012', '%m/%d/%Y')
        # save strptime as a variable that we can call on dates in the file later to convert them to datetime objects
        my_date = datetime.datetime.strptime

        # counter for 'ao's in the file
        found = 0
        # counter dict for each year we care about counting in the file
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        # iterate through 1,000,000 rows
        for row in reader:
            # store each date from the date column as a datetime object
            row_date = my_date(row[5], '%m/%d/%Y')
            # count each year 2013-2018 and save to year_count dictionary
            if row_date > date:
                if row_date.year == 2013:
                    year_count["2013"] += 1
                if row_date.year == 2014:
                    year_count["2014"] += 1
                if row_date.year == 2015:
                    year_count["2015"] += 1
                if row_date.year == 2016:
                    year_count["2016"] += 1
                if row_date.year == 2017:
                    year_count["2017"] += 1
                if row_date.year == 2018:
                    year_count["2018"] += 1
            # count number of 'ao's in text of column 6
            if "ao" in row[6]:
                found += 1

        # left these in the file just to be able to view the output
        print(year_count)
        print(f"'ao' was found {found} times")

    # timestamp when function is done running
    end = datetime.datetime.now()

    # output of function: timestamps for start and end, plus count of years and 'ao'
    return (start, end, year_count, found)


def main():
    """
    Main function to run file, should be called in name == main line when executing the program
    """
    filename = "exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    # run timeit to measure the time it takes to run the program, "number" is number of times running the program
    print(timeit("analyze('exercise.csv')", globals=globals(), number=10))
    # main()
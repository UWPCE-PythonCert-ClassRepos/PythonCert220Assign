"""
    Lesson06 Assignment
    Cleaned up version of poor_perf.py file.
"""

from timeit import timeit
import datetime
import csv
# from line_profiler import LineProfiler



def analyze(filename):
    """
        Function imports csv file, loops through the years converting
        them from string format to proper date formatting object , saves
        count in a dict for years 2013-2018, and counts how many times
        'ao' shows up in the file.
        :param: csv file
        :return: Start date, end date, frequency of years 2013-2018,
        frequency of "ao"


    """

    # Timestamp for start of function
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        # Skips header, otherwise datetime will not work
        next(reader, None)

        # Converts string date in a proper datetime object
        # dates after 01/01/2012
        # Datetime allows clean conversion of datetime object if
        # date format is not all formatted the same
        # Datetime extends run time considerably, but for one dirty run,
        # we output clean data
        date = datetime.datetime.strptime('01/01/2012', '%m/%d/%Y')
        my_date = datetime.datetime.strptime
        # Orignial comprehension
        # new_ones = [(row[5], row[0]) for row in reader if my_date(row[5], '%m/%d/%Y') > date]

        # Counter for "ao"
        found = 0
        # Dict counter for each year in the file that we are care about
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        # How can I make this a comprehension if possible?
        # Iterates through 1 million rows
        for row in reader:
            # Stores each date as datetime object
            row_date = my_date(row[5], '%m/%d/%Y')
            # Counts for each year stored in a dict
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

            # 'ao' counter for entire firle
            if "ao" in row[6]:
                found += 1

        print(year_count)
        print(f"ao was found {found} times")

        # Ends timestamp for function
        end = datetime.datetime.now()

        return (start, end, year_count, found)


def main():
    """
        Main function to run csv file.
    """
    filename = "exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    # Timeit outputs the time it takes to run the file a "number"
    # amount of times
    print(timeit("analyze('exercise.csv')", globals=globals(), number=1))

    # main()

    ## Option to use other than cProfile
    # lp = LineProfiler()
    # lp_wrapper = lp(analyze)
    # lp_wrapper("exercise.csv")
    # lp.print_stats()

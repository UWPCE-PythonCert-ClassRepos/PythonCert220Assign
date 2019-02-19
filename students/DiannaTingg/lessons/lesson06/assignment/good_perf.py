"""
Lesson 06 Assignment
"""

import datetime
import csv
# from timeit import timeit
# from line_profiler import LineProfiler


def analyze(filename):
    """
    Returns certain statistics for a file.
    :param filename: csv file
    :return: Start date, end date, frequency of years 2013-2018, frequency of "ao"
    """
    start = datetime.datetime.now()

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        next(reader, None)  # Skip the header row.

        year_count = {}

        found = 0

        for row in reader:
            if "2012" < row[5][-4:] < "2019":
                year_count[row[5][-4:]] = year_count.get(row[5][-4:], 0) + 1

            if "ao" in row[6]:
                found += 1

        # print(year_count)

        # print(f"'ao' was found {found} times")

        end = datetime.datetime.now()

    return start, end, year_count, found


# def main():
#     filename = "exercise.csv"
#     analyze(filename)


if __name__ == "__main__":
    analyze("exercise.csv")

    # main()

    # print(timeit("analyze('exercise.csv')", globals=globals(), number=10))

    # lp = LineProfiler()
    # lp_wrapper = lp(analyze)
    # lp_wrapper("exercise.csv")
    # lp.print_stats()

import datetime
import csv
import collections
from dateutil.parser import parse


def analyze(filename):
    """
    Analyzes a file and produces a count of years and the number of times "ao" was found
    """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        good_years = (row[5][6:] for row in reader if row[5][6:] > "2012" and row[5][6:] < "2019")
        year_count = collections.Counter(good_years)
        csvfile.seek(0)
        found = len([1 for line in reader if 'ao' in line[6]])
    end = datetime.datetime.now()
    time = end - start
    return time.total_seconds(), year_count, found


def analyze_2(filename):
    """
    Same as above function, but only reads file once
    """
    start = datetime.datetime.now()
    good_years = collections.defaultdict(lambda: 0)
    found = 0
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        important_data = ((row[5][6:], row[6]) for row in reader)
        for data in important_data:
            if data[0] > "2012" and data[0] < "2019":
                good_years[data[0]] += 1
            if 'ao' in data[1]:
                found += 1
    end = datetime.datetime.now()
    time = end - start
    return time.total_seconds(), good_years, found

def analyze_3(filename):
    """
    Same as above function, but only goes through data once
    """
    start = datetime.datetime.now()
    good_years = collections.defaultdict(lambda: 0)
    found = 0
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for data in reader:
            if data[5][6:] > "2012" and data[5][6:] < "2019":
                good_years[data[5][6:]] += 1
            if 'ao' in data[6]:
                found += 1
    end = datetime.datetime.now()
    time = end - start
    return time.total_seconds(), good_years, found


def analyze_4(filename):
    """
    Just open the file and parse commas, don't use csv library
    """
    start = datetime.datetime.now()

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
        row = csvfile.readline()
        row = csvfile.readline()
        while row:
            comma_index = row.rfind(",")
            sentence = row[comma_index + 1:]
            year = row[comma_index - 4: comma_index]
            if year in year_count:
                year_count[year] += 1
            if "ao" in sentence:
                found += 1
            row = csvfile.readline()
    end = datetime.datetime.now()
    time = end - start
    return time.total_seconds(), year_count, found


print(analyze("exercise.csv"))
print(analyze_2("exercise.csv"))
print(analyze_3("exercise.csv"))
print(analyze_4("exercise.csv"))

"""
good performing, perfectly written module :)

"""


import datetime
from dateutil.parser import parse
from datetime import datetime as dt

def analyze(filename):
    '''
    Reads and analyzes data from the given file

    :param filename: file path of file to analyze
    '''
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
        # skip the first record
        row = csvfile.readline()
        while row:
            comma_index = row.rfind(",")
            sentence = row[comma_index + 1:]
            year = row[comma_index - 4: comma_index]

            # Date Parsing options
            # comma_date_index = row.rfind(",", comma_index - 20, comma_index -1)

            # dateutils.parse = 71s
            # year = str(parse(row[comma_index - 10: comma_index]).year)

            # OR datetime.strptime = 16.5s
            # try:
            #     year = str(dt.strptime(row[comma_date_index + 1: comma_index], '%m/%d/%Y').year)
            # except ValueError as valueError:
            #     print(valueError)
                
            if year in year_count:
                year_count[year if year != "2018" else "2017"] += 1
            if "ao" in sentence:
                found += 1
            row = csvfile.readline()

    print(year_count)
    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    '''
    Main execution function
    '''
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()

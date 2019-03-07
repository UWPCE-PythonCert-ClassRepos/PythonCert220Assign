#Tim Pauley
#Assignment 06
#Date: Feb 15 2019
#Update: Feb 20 2019

#Poor Version

'''
Assignment 06 Description

Here is what you need to do:

The assignment repository for this lesson contains a file with 1 million 
records and a module that reads that file.

The module is badly written and probably can be made to run more quickly 
and efficiently!

You will look at the code and may immediately form a judgment about where 
performance can be improved. Do not be tempted to make immediate changes!
Be sure to use an evidence based approach, and show, with data, how you 
were able to make improvements.

Rewrite the module to improve performance. Provide evidence to demonstrate 
the improvement.

Your new module should be called good_perf.py, it should use identical 
input and produce identical output to poor_perf.py

'''



"""
Test file to check that output of good_perf.py is the same as code is refactored.
"""

import good_perf as gp

result_dict = {'2013': 5911, '2014': 5854, '2015': 5994, '2016': 5762, '2017': 5789, '2018': 5811}
ao_count = 63395

def test_output_of_good_perf_remains_same():
    result = gp.analyze("exercise.csv")

    assert result[2] == result_dict
    assert result[3] == ao_count
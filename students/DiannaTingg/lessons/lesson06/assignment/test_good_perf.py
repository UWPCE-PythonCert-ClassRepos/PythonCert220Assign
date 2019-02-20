"""
Lesson 06 Assignment
Tests
"""

import good_perf as gp


def test_analyze():
    """
    Makes sure that my refactored code still works properly.
    """
    result = gp.analyze("exercise.csv")

    year_dict = {'2013': 5911, '2014': 5854, '2015': 5994, '2016': 5762, '2017': 5789, '2018': 5811}
    ao_count = 63395

    assert result[2] == year_dict
    assert result[3] == ao_count

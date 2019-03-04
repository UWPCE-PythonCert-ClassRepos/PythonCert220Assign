import good_perf as gp

result_dict = {'2013': 5911, '2014': 5854, '2015': 5994, '2016': 5762, '2017': 5789, '2018': 5811}
ao_count = 63395


def test_analyze_stays_the_same():
    result = gp.analyze("exercise.csv")

    assert result[2] == result_dict
    assert result[3] == ao_count

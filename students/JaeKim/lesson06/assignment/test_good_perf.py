import good_perf as gp

def test_analyze():
    results = gp.analyze("data/exercise.csv")

    assert results[2] == {'2013': 5911, '2014': 5854, '2015': 5994, '2016': 5762, '2017': 5789, '2018': 5811}
    assert results[3] == 63395

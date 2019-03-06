from poor_perf import analyze as poor
from good_perf import analyze as good
import timeit as timer

def test_check_time():
    filename = "data/exercise.csv"
    print("Poor:")
    print(timer.timeit(stmt= "poor(filename)",
        setup= "from poor_perf import analyze as poor; filename = 'data/exercise.csv'", number=1))
    print("Good:")
    print(timer.timeit(stmt="good(filename)",
        setup= "from good_perf import analyze as good;filename = 'data/exercise.csv'", number=1))

if __name__ == '__main__':
    check_time()
import timeit as timer


def check_time():
    filename = "data/exercise.csv"
    print("Parallel:")
    print(
        timer.timeit(
            stmt="parallel()",
            setup="from parallel import results_sum_parallel as parallel",
            number=100))
    print("Linear:")
    print(
        timer.timeit(
            stmt="linear()",
            setup="from parallel import results_sum_linear as linear",
            number=100))


if __name__ == '__main__':
    check_time()

from multiprocessing.pool import ThreadPool
from database import import_data
from database import show_available_products


def run_parallel():
    """
    Run the import data in parallel
    """
    pool = ThreadPool()
    files = ["customer_data.csv", "product_data.csv", "rental_data.csv"]
    return (pool.apply_async(import_data, ("dat", file)) for file in files)


def run_linear():
    """
    Run the import data in linear
    """
    files = ["customer_data.csv", "product_data.csv", "rental_data.csv"]
    return (import_data("dat", file) for file in files)


def results_sum_parallel():
    """
    Sum the results of the parallel run
    """
    result_list = [thread.get() for thread in run_parallel()]
    return (sum(i for i, j in result_list), sum(j for i, j in result_list))


def results_sum_linear():
    """
    Sum the results of the linear run
    """
    result_list = [result for result in run_linear()]
    return (sum(i for i, j in result_list), sum(j for i, j in result_list))


def run_contention():
    """
    Demonstrates a possible contention of data
    """
    pool = ThreadPool(processes=1)
    thread_generator = (pool.apply_async(import_data,
                                         ("dat", "product_data.csv")),
                        pool.apply_async(import_data,
                                         ("dat", "rental_data.csv")),
                        pool.apply_async(show_available_products))
    result_list = [thread.get() for thread in thread_generator]
    pool.close()
    return result_list


if __name__ == '__main__':
    print(run_contention())

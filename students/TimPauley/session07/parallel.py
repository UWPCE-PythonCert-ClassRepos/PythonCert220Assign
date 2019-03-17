#Tim Pauley
#Date March 02 2019
#Assignment 07
#File Name: parallel.py

#Concurrency & Async Programming


'''
Assignment
HP Norton is having success with their new computer system written in 
Python. So much success, in fact, that the way they have had some of 
their systems written is starting to introduce processing bottlenecks, 
and therefore delays for users.

In this lesson’s assignment, we are going to apply techniques beyond 
vertical scaling (upgrading servers) to help maximize their application 
performance.

You should address the following general requirements:

As a user of the HP Norton systems, I need to be confident that the 
system will perform sufficiently rapidly that responses are almost 
instantaneous, and I am not kept waiting for the system to complete 
its processing. I feel the system now is too slow, and I want to see 
if improvements can be made without having to upgrade our hardware.
Here is what you need to do:

TO DO

1. Demonstrate with real profile data the time taken to run your existing 
customer and product add / update logic.

2. Amend the add and update logic for both customers and products so that 
it can process these in parallel. Your module should launch the updates 
o both databases simultaneously. Provide real timing data for your new 
approach.

3. Compare and contrast parallel vs. linear performance and recommend to 
management if a change is worthwhile.

4. To show you have thought through your design, create and provide an 
example of where the program fails due to contention and explain why 
in code comments, and how that will be avoided when the system is 
running.

Submit

You will submit two modules: linear.py and parallel.py

Outline

Each module will return a list of tuples, one tuple for customer and 
one for products. Each tuple will contain 4 values: 

1. the number of records processed (int)
2. the record count in the database prior to running (int)
3. the record count after running (int), and the time taken to run 
the module (float).

You will also submit a text file containing your findings.
Other requirements:

1. Your code should not trigger any warnings or errors from Pylint.
Testing

Make sure your tests run as expected.
Submission

You will need to submit linear.py, parallel.py, your brief bullet point notes on findings and recommendations called findings.txt, and any test files you develop.
Tips
'''

from multiprocessing.pool import ThreadPool
from database import import_data
from database import show_available_products


def run_parallel():
    """
    This is where I run the import data in parallel
    """
    pool = ThreadPool()
    files = ["customer_data.csv", "product_data.csv", "rental_data.csv"]
    return (pool.apply_async(import_data, ("dat", file)) for file in files)


def run_linear():
    """
    This is where I import data in linear
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
    '''
    This is where the main method is run
    '''
    print(run_contention())

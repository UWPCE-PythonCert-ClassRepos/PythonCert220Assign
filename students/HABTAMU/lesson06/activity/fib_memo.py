from functools import lru_cache
import timeit
# startNumber = int(raw_input("Enter the start number here "))
# endNumber = int(raw_input("Enter the end number here "))

# @lru_cache(maxsize=32)
# def fib(n):
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fib(n-2) + fib(n-1)

# @lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

# print(fib.cache_info())
print(timeit.timeit(stmt="print(fib(100))", globals=globals(), number=5))
#print map(fib, range(startNumber, endNumber))

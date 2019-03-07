from functools import lru_cache
import timeit



def fib(n):
   if n == 0:
       return 0
   elif n == 1:
       return 1
   else:
       return fib(n-1) + fib(n-2)

#print(timeit.timeit(stmt="print(fib(100))", globals=globals(), number=5))

fib = lru_cache(maxsize=None)(fib)

print(timeit.timeit(stmt="print(fib(100))", globals=globals(), number=5))

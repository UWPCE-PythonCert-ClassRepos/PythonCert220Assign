# Profileling tutorial
#rriehle

from timeit import timeit as timer

repititions = 10000
my_range = 10000

lower_limit = my_range / 2

my_list = list(range(my_range))

def multiply_by_two(x):
    return x * 2

def greater_than_lower_limit(x):
    return x > lower_limit


print("\n\nmap_filter_with_functions")
print(timer(
    'map_filter_with_functions=map(multiply_by_two, filter(greater_than_lower_limit, my_list))',
    globals=globals(),
    number=repititions
))
# 0.004174136000000002

# map_filter_with_functions = map(multiply_by_two, filter(greater_than_lower_limit,my_list))
# print(*map_filter_with_functions)

print("\n\nmap_filter_with_lambda")
print(timer(
    'map_filter_with_lambda=map(lambda x: x * 2, filter(lambda x: x > lower_limit, my_list))',
    globals=globals(),
    number=repititions
))
# 0.025728053

# map_filter_with_lambda = map(
#     lambda x: x * 2, filter(lambda x: x > lower_limit, my_list))
# print(*map_filter_with_lambda)

print("\n\ncomprehension")
print(timer(
    'comprehension = [x * 2 for x in my_list if x > lower_limit]',
        globals=globals(),
        number=repititions
))
# 8.468971451

# comprehension = [x * 2 for x in my_list if x > lower_limit]
# print(*comprehension)

print("\n\ncomprehension_with_function")
print(timer(
    'comprehension_with_function = [multiply_by_two(x) for x in my_list if greater_than_lower_limit(x)]',
    globals=globals(),
    number=repititions
))
# 21.205117949999998

# comprehension_with_function = [multiply_by_two(x) for x in my_list if greater_than_lower_limit(x)]
# print(*comprehension_with_function)

print("\n\ncomprehension_with_lambda")
print(timer(
    'comprehension_with_lambda = [(lambda x: x * 2)(x) for x in my_list if (lambda x: x > lower_limit)(x)]',
    globals=globals(),
    number=repititions
))
# 30.825075997

# comprehension_with_lambda = [(lambda x: x * 2)(x) for x in my_list if (lambda x: x > lower_limit)(x)]
# print(*comprehension_with_lambda)


# $ python MapFilterTime.py

# map_filter_with_functions
# 0.0035826479999999973


# map_filter_with_lambda
# 0.004742512999999997


# comprehension
# 9.970715746


# comprehension_with_function
# 26.375267500999996


# ccomprehension_with_lambda
# 36.164358777

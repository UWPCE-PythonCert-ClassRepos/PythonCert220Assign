def fibonacci(max):
    a, b = 0, 1
    while a < max:
        yield a
        a, b = b, a+b
if __name__ == '__main__':
    # Create generator of fibonacci numbers
    fibonacci_generator = fibonacci(1000000)
    # print out all the sequence
    for fibonacci_number in fibonacci_generator:
        print(fibonacci_number)

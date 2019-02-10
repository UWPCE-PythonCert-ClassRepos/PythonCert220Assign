class fibonacci:
    def __init__(self, max=1000000):
        self.a, self.b = 0, 1
        self.max = max
    def __iter__(self):
        # Return the iterable object (self)
        return self
    def __next__(self):
        # To stop the iteration we just need to raise
        # a StopIteration exception
        if self.a > self.max:
            raise StopIteration
        # save the value that has to be returned
        value_to_be_returned = self.a
        # calculate the next values of the sequence
        self.a, self.b = self.b, self.a + self.b
        return value_to_be_returned

if __name__ == '__main__':
    MY_FIBONACCI_NUMBERS = fibonacci()
    for fibonacci_number in MY_FIBONACCI_NUMBERS:
        print(fibonacci_number)

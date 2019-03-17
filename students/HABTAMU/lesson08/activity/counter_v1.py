def counter(start=0):
    count = start
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

default_counter = counter()
mysecondcounter = counter()
custom_counter = counter(3)

default_counter()

mysecondcounter()

#custom_counter(3)

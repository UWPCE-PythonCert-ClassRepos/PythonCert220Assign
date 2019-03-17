def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

mycounter = counter()
mysecondcounter = counter()

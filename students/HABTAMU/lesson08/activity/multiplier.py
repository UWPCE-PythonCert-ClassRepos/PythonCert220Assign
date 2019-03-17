def make_multiplier(n):
    def multiply(x):
        return x * n
    return multiply


times3 = make_multiplier(3)
times3(4) # 12


times5 = make_multiplier(5)
times5(4) # 20

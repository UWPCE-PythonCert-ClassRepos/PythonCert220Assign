from functools import partial
def multiplier(x ,n=3):
    return x * n


double_it = partial(multiplier, 2)
quadruple_it = partial(multiplier, 4)

double_it(4)

quadruple_it(4)

class Dummy:
    pass

my_obj = Dummy()

setattr(my_obj, 'Namde', 'wat')

print(vars(my_obj))
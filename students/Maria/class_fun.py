class MyMeta(type):
    def __new__(meta, name, bases, dct):
        print('-----------------------------------')
        print("Allocating memory for class", name)
        print(meta)
        print(bases)
        print(dct)
        return super(MyMeta, meta).__new__(meta, name, bases, dct)
    def __init__(cls, name, bases, dct):
        print('-----------------------------------')
        print("Initializing class", name)
        print(cls)
        print(bases)
        print(dct)
        super(MyMeta, cls).__init__(name, bases, dct)
    def __call__(cls, *args, **kwargs):
        print('__call__ of {}'.format(cls))
        print('__call__ of *args = {}'.format(args))
        return type.__call__(cls, *args, **kwargs)

class MyKlass(metaclass=MyMeta):

    def __init__(self, a, b):
        print('MyKlass object iwht a={}, b={}'.format(a, b))

    def foo(self, param):
        pass

    barattr = 2

#print('going to create foo now...')
#foo = MyKlass(1, 2)



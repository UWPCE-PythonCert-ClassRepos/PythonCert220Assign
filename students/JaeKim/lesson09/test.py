
def d(msg='my default message'):
    def decorator(func):
        def newfn():
            print(msg)
            return func()
        return newfn
    return decorator

@d(MESSAGE)
def hello():
    print('hello world !')

@d()
def hello2():
    print('also hello world')

hello2()
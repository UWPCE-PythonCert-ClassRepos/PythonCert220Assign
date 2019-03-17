fun_list = []

def collect_fun(func):
	print('collecting fun {}'.format(func.__name__))
	fun_list.append(func)

@collect_fun
def fun1():
	print("hello")

@collect_fun
def fun2():
	print("goodbye")

def fun3():
	print("whatever")	

print(fun_list)
for fun in fun_list:
	fun()

				
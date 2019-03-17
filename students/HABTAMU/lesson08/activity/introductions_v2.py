from functools import partial
from introductions import introduce_person
simple_intro= partial(introduce_person, age=10, job='student', location='Seattle')
#simple_intro('Alison')


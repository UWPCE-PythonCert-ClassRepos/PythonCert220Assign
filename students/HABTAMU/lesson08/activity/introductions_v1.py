def get_simple_intro(age, job, location):
    def simple_introduction(name):
        return "This is %s, a %d-year-old %s living in %s" % (name, age, job, location)
    return simple_introduction



#simple_intro = get_simple_intro(10, 'student', 'Seattle')
#simple_intro('Maya')
#simple_intro('Alison')


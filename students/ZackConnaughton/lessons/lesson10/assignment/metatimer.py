import types
import time

class Timer:
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def csv_output(self, function_name, time_data):
        with open('timings.txt', 'a') as append_file:
            append_file.write(f"{function_name},{time_data:.5f}\n")

def timefunc(fn, *args, **kwargs):

    def fncomposite(*args, **kwargs):
        timer = Timer()
        timer.start()
        rt = fn(*args, **kwargs)
        timer.stop()
        timer.csv_output(fn.__name__, timer.elapsed)
        return rt
    return fncomposite


class Timed(type):

    def __new__(cls, name, bases, attr):
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = timefunc(value)
        return super(Timed, cls).__new__(cls, name, bases, attr)

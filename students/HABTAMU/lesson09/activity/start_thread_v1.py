#!/usr/bin/python
# Starting a New Thread
# https://www.tutorialspoint.com/python/python_multithreading.htm

import _thread
import time
a_lock = _thread.allocate_lock()

with a_lock:
    # Define a function for the thread
    def print_time( threadName, delay):
       count = 0
       while count < 5:
          time.sleep(delay)
          count += 1
          print("%s: %s" % ( threadName, time.ctime(time.time()) ))

    # Create two threads as follows
    try:
       _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
       _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
    except:
       print("Error: unable to start thread")

    while 1:
       pass

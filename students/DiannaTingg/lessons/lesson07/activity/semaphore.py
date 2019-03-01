"""
Lesson 07 Activity
Locking Exercise
Multiple threads in the script write to stdout, and their output gets jumbled.
"""

import random
import sys
import threading
import time

LOCK = threading.Semaphore(2)


def write():
    """
    Includes a semaphore to allow two threads access at once.
    """
    with LOCK:
        sys.stdout.write("%s writing.." % threading.current_thread().name)
        time.sleep(random.random())
        sys.stdout.write("..done\n")


for i in range(25):
    thread = threading.Thread(target=write)
    thread.start()
    time.sleep(.1)

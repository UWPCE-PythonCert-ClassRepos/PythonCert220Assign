"""
Lesson 07 Activity
Locking Exercise
Multiple threads in the script write to stdout, and their output gets jumbled.
"""

import random
import sys
import threading
import time

LOCK = threading.Lock()


def write():
    """
    Includes a locking mechanism to give each thread exclusive access to stdout.
    """
    with LOCK:
        sys.stdout.write("%s writing.." % threading.current_thread().name)
        time.sleep(random.random())
        sys.stdout.write("..done\n")


THREADS = []

for i in range(25):
    thread = threading.Thread(target=write)
    thread.daemon = True  # allow ctrl-c to end
    thread.start()
    THREADS.append(thread)
    time.sleep(.1)

for t in THREADS:
    t.join()

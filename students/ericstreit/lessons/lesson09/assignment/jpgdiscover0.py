
from pathlib import Path
import os

# CHEATING
# this does it but using builtin recursion using the os.walk function

def jpegdiscovery(root_path):
    for root, dirs, files in os.walk(root_path):
        for name in files:
            if name.endswith('.png'):
                print (os.path.join(root, name))

jpegdiscovery('c:\\assignment_test')

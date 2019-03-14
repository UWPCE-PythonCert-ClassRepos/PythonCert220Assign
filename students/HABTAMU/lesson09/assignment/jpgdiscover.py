
'''
A discovery program using recursion, that works from a parent directory called images provided on the command line. 
:params: parent directory 
:return: lists structured dir recursively go through directories looking for pngs
'''

import sys
import os
from pathlib import Path

def png_discovery(directory, png_paths=None):
    if png_paths is None:
        png_paths = []

    current_list = [directory, []]
    # for filename in os.listdir(directory):
    for filename in directory.iterdir():
        if filename.is_dir():
            png_discovery(filename, png_paths)
        elif filename.name.endswith(".png"):
            current_list[1].append(filename.name)

    if current_list[1]:
        png_paths.extend(current_list)
    return png_paths


if __name__ == '__main__':
    directory = Path.cwd()
    print(*png_discovery(directory), sep='\n')



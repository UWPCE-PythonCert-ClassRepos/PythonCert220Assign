"""
Recursively go through directories looking for pngs
"""
import os


def jpegdiscovery(directory, png_paths=None):
    #import pdb; pdb.set_trace()
    if not png_paths:
        png_paths = []
    for filename in os.listdir(directory):
        if os.path.isdir(filename):
            png_paths.extend(jpegdiscovery(filename, png_paths))
        if filename.endswith(".png"):
            png_paths.append(os.path.abspath(filename))
    return png_paths


print(jpegdiscovery(os.getcwd()))

"""  This is the third part of the assignment 10 with recursively adds files to a dict if a png"""
import os
def jpegdiscovery(directory, png_paths=None):
    #import pdb; pdb.set_trace()
    if not png_paths:
        png_paths = []
    for filename in os.listdir(directory):
        if os.path.isdir(filename):
            png_paths.extend(jpegdiscovery(filename, png_paths))
        if filename.endswith(".jpg"):
            png_paths.append(os.path.abspath(filename))
    return png_paths

if __name__ == "__main__":
    print(jpegdiscovery(os.getcwd()))



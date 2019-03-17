# """ Recursively go through directories looking for pngs """

import os

def jpg_discovery(directory, png_paths=None):
    if png_paths is None:
        png_paths = []
    for filename in os.listdir(directory):
        path_join = os.path.join(directory, filename)
        # if os.path.isdir(filename):
        if os.path.isdir(path_join):
            jpg_discovery(path_join, png_paths)
            # png_paths.extend(jpg_discovery(filename, png_paths))
        if filename.endswith(".py"):
            png_paths.append(path_join)
    return png_paths

print(jpg_discovery(os.getcwd()))


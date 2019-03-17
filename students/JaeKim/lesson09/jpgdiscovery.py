"""
Recursively go through directories looking for pngs
"""
import os


# def jpegdiscovery(directory, png_paths=None):
#     #import pdb; pdb.set_trace()
#     if not png_paths:
#         png_paths = []
#     for filename in os.listdir(directory):
#         if os.path.isdir(os.path.join(directory, filename)):
#             print(os.path.join(directory, filename))
#             png_paths.extend(jpegdiscovery(filename, png_paths))
#         if filename.endswith(".png"):
#             png_paths.append(os.path.abspath(filename))
#     return png_paths

def jpegdiscovery(directory, png_paths=None):
    if png_paths is None:
        png_paths = []
    current_list = [directory, []]

    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            jpegdiscovery(path, png_paths)
        elif path.endswith(".png"):
            current_list[1].append(filename)

    if current_list[1]:
        png_paths.extend(current_list)

    return png_paths

print(jpegdiscovery(os.getcwd()))
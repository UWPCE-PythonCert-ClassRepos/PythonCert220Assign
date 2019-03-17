# """ Recursively go through directories looking for pngs """

import os
# def jpegdiscovery(directory, png_paths=None):
#     if not png_paths:
#         png_paths = []
#     for filename in os.listdir(directory):
#         if os.path.isdir(filename):
#             png_paths.extend(jpegdiscovery(filename, png_paths))
#         if filename.endswith(".png"):
#             png_paths.append(os.path.abspath(filename))
#     # if filename is None:
#     # print(png_paths)
#     return png_paths


#     # for root, dirs, files in os.walk(directory):
#     #     # import pdb;pdb.set_trace()
#     #     if os.path.isdir(filename):
#     #         jpegdiscovery(filename, png_paths)
#     #     if filename.endswith(".png"):
#     #         png_paths.append(os.path.abspath(filename))
#     # return png_paths

# print(jpegdiscovery(os.getcwd()))


def jpg_discovery(directory, png_paths=None):
    if not png_paths:
        png_paths = []
    for filename in os.listdir(directory):
        if os.path.isdir(filename):
            png_paths.extend(jpg_discovery(filename, png_paths))
        if filename.endswith(".py"):
            png_paths.append(os.path.abspath(filename))
    return png_paths


print(jpg_discovery(os.getcwd()))

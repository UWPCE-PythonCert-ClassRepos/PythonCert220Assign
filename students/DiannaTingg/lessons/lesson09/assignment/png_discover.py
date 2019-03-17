"""
Lesson 09 Assignment - Part 3
Recursion
"""

import os

# pylint: disable-msg=line-too-long


def png_discover(directory, png_list=None):
    """
    Recursively searches a parent directory and all subdirectories for png files.
    :param directory: Parent directory for image search.
    :param png_list: Default is set to None
    :return: A list of lists.  Each list contains the directory and a list of the png files in that directory.
    """

    if png_list is None:
        png_list = []

    current_list = [directory, []]

    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            png_discover(os.path.join(directory, item), png_list)

        if item.endswith(".png"):
            current_list[1].append(item)

    if current_list[1]:  # Check if there are png files in current_list.
        png_list.extend(current_list)

    return png_list


print("List of directories with PNG files:")

IMAGE_LIST = png_discover(os.path.join(os.getcwd(), "data"))

for sublist in IMAGE_LIST:
    print(sublist)

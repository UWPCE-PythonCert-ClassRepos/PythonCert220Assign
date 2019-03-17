"""
File explorer that runs recursively down through a file tree collecting image file paths into a list
"""

import os

IMAGE_LIST = []
PATH = "data"

def get_images(path):
    directory = (os.getcwd() + "/" + path)
    images = []
    for item in (os.listdir(directory)):
        if '.png' in item:
            images.append(item)
        if os.path.isdir(directory + "/" + item):
            get_images(path + "/" + item)
    if images:
        IMAGE_LIST.append([path, images])

get_images(PATH)
print(IMAGE_LIST)

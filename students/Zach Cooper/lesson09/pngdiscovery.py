"""
Recursively go through directories looking for pngs down the file treee
"""
import os


def png_photo_discovery(directory, png_paths=None):
    """
        Search directory using recursion to pull and find all png files
        :output: return in a dictionary
    """

    if png_paths is None:
        png_paths = []

    current_list = [directory, []]

    for item in os.listdir(directory):
        # path_join = os.path.join(directory, item)
        if os.path.isdir(os.path.join(directory, item)):
            png_photo_discovery(os.path.join(directory, item), png_paths)

        elif item.endswith(".png"):  # Append photos with .png ending
            current_list[1].append(item)

    if current_list[1]:
            png_paths.extend(current_list)

    return png_paths


print("Directories with files ending in .png:")
print(png_photo_discovery(os.getcwd()))

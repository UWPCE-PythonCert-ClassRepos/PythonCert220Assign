"""
Recursively go through directories looking for pngs
"""
import os


def jpegdiscovery(directory):
    """
    Recursively adds files to a dict if a png
    """
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isdir(file_path):
            jpegdiscovery(file_path)
        elif file.endswith(".png"):
            if directory in file_dict.keys():
                file_dict[directory].append(file)
            else:
                file_dict[directory] = [file]


if __name__ == "__main__":
    """
    Correctly formats the output
    """
    file_dict = {}
    jpegdiscovery(os.getcwd())
    file_list = [[file, file_dict[file]] for file in file_dict]
    print(file_list)

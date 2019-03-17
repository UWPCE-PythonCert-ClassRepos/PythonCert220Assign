import os

def jpegdiscovery(directory, png_paths=None):
    if png_paths is None:
        png_paths = []
    png_list = [directory, []]

    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if os.path.isdir(path):
            jpegdiscovery(path, png_paths)
        elif path.endswith(".png"):
            png_list[1].append(f)

    if png_list[1]:
        png_paths.extend(png_list)

    return png_paths

print(jpegdiscovery(os.getcwd()))

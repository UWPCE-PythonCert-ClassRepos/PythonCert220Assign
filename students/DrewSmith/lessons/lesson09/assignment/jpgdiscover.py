'''
Recursively go through directories looking for pngs
'''


from pathlib import Path

def jpgdiscovery(directory, png_paths=None):
    '''
    Recursively find all PNG image files in a directory
    :param directory: pathlib directory path to search
    :param png_paths: list used to build return list
    '''
    if png_paths is None:
        png_paths = []
    
    current_list = [directory, []]
    for path in directory.iterdir():
        if path.is_dir():
            jpgdiscovery(path, png_paths)
        elif path.name.endswith(".png"):
            current_list[1].append(path.name)

    if current_list[1]:
        png_paths.extend(current_list)
    return png_paths

if __name__ == '__main__':
    print(*jpgdiscovery(Path.cwd()), sep='\n')

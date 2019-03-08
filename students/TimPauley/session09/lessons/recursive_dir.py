'''
Object

Recursively go through directories and find jpeg's
'''

import os

def jpegdiscovery(directory, png_paths=None):
	if not png_paths:
		png_paths = []
	for filename in os.listdir(directory):
		#import pdb; pdb.set_trace()
		if os.path.isdir(filename):
			png_paths = jpegdiscovery(filename, png_paths)
		if filename.endswith(".png"):
			png_paths.append(as.path.abspath(filename))

print(jpegdiscovery(as.get()))

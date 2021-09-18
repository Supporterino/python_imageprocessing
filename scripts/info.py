#!/usr/bin/env python3

from os import listdir
from os.path import join, isfile
from PIL import Image

path = "/mnt/ssd/python_imageprocessing/4x"

files = [f for f in listdir(path) if isfile(join(path, f))]

h_counter = 0
w_counter = 0
counter = 0

for file in files:
    print(f'Picture: {join(path, file)}')
    im = Image.open(join(path, file))
    w, h = im.size
    print(f'Size: W: {w}, H: {h}')
    if (w < 1920):
        w_counter += 1
    if (h < 1080):
        h_counter += 1
    if (w < 1920 and h < 1080):
        counter += 1

print(f'{counter} pictures too small')
print(f'{h_counter} pictures not high enough')
print(f'{w_counter} pictures not wide enough')

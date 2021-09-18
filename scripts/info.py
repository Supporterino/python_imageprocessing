#!/usr/bin/env python3

from os import listdir
from os.path import join, isfile
from PIL import Image

path = "/mnt/ssd/alisa_photos/2x"

files = [f for f in listdir(path) if isfile(join(path, f))]

counter = 0

for file in files:
    print(f'Picture: {join(path, file)}')
    im = Image.open(join(path, file))
    w, h = im.size
    print(f'Size: W: {w}, H: {h}')
    if (w < 1080 or h < 1080):
        counter += 1

print(f'{counter} pictures too small')

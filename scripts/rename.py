#!/usr/bin/env python3

from os import listdir, rename
from os.path import join, isfile

path = "/mnt/ssd/alisa_photos/pngify"

files = [f for f in listdir(path) if isfile(join(path, f))]

counter = 0

for file in files:
    rename(join(path, file), join(path, f'{counter}.png'))
    counter += 1
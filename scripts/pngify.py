#!/usr/bin/env python3

from os import listdir
from os.path import join, isfile
from PIL import Image
from multiprocessing import Pool

path = "/mnt/ssd/alisa_photos/unprocessed"
output = "/mnt/ssd/alisa_photos/pngify"

files = [f for f in listdir(path) if isfile(join(path, f))]

def write(file):
    print(f'Processing {join(path, file)}')
    im = Image.open(join(path, file))
    im.save(join(output, file))

if __name__ == '__main__':
    pool = Pool()
    pool.map(write, files)
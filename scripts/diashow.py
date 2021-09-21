#!/usr/bin/env python3

from os import listdir
from os.path import join, isfile
import cv2
import random

WIDTH = 1920
HEIGHT = 1080


def write(filename, frames):
    out = None

    try:
        for frame in frames:
            if not out:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(filename, fourcc, 30, (WIDTH, HEIGHT))

            out.write(frame)

    finally:
        out and out.release()


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized

def make_16x9(im):
    height, width, _ = im.shape

    print(height, width)

    desired_width = 16 * (height / 9)
    delta_w = desired_width - width
    delta_h = 0
    top, bottom = 0, 0
    left, right = int(delta_w/2) + 25, int(delta_w-(delta_w/2)) + 25

    
    print(top, bottom, left, right)
    color = [0, 0, 0]
    new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,
        value=color)
    
    return new_im

class Image:
    def __init__(self, filename, time=500):
        self.time = time
        self.shifted = 0.0
        self.img = make_16x9(cv2.imread(filename))
        self.height, self.width, _ = self.img.shape
        if self.width < self.height:
            print('Height bigger')
            print(f'Raw dim. height:{self.height}, width:{self.width}')
            self.height = int(self.height*WIDTH/self.width)
            self.width = WIDTH
            print(f'Setted dim. height:{self.height}, width:{self.width}')
            self.img = image_resize(self.img, width=WIDTH)
            self.shift = self.height - HEIGHT
            print(f'Shift: {self.shift}')
            self.shift_height = True
        else:
            print('Width bigger')
            print(f'Raw dim. height:{self.height}, width:{self.width}')
            self.width = int(self.width*HEIGHT/self.height)
            self.height = HEIGHT
            print(f'Setted dim. height:{self.height}, width:{self.width}')
            self.img = image_resize(self.img, height=HEIGHT)
            self.shift = self.width - WIDTH
            print(f'Shift: {self.shift}')
            self.shift_height = False
        self.delta_shift = self.shift/self.time

    def reset(self):
        if random.randint(0, 1) == 0:
            self.shifted = 0.0
            self.delta_shift = abs(self.delta_shift)
        else:
            self.shifted = self.shift
            self.delta_shift = -abs(self.delta_shift)

    def get_frame(self):
        if self.shift_height:
            roi = self.img[int(self.shifted):int(self.shifted) + HEIGHT, :, :]
        else:
            roi = self.img[:, int(self.shifted):int(self.shifted) + WIDTH, :]
        # self.shifted += self.delta_shift
        # if self.shifted > self.shift:
        #     self.shifted = self.shift
        # if self.shifted < 0:
        #     self.shifted = 0
        return roi


def process(files_to_process, in_path, out_file):
    images = []
    frames_out = []
    removed = 0

    for filename in files_to_process:
        print(join(in_path, filename))

        img = Image(join(in_path, filename))

        if (img.shift >= 0):
            images.append(img)
        else:
            removed += 1

    prev_image = images[random.randrange(0, len(images))]
    prev_image.reset()

    for img in images:
        img.reset()

        for i in range(50):
            alpha = i/50
            beta = 1.0 - alpha
            dst = cv2.addWeighted(img.get_frame(), alpha,
                                  prev_image.get_frame(), beta, 0.0)

            frames_out.append(dst)

        prev_image = img
        for _ in range(100):
            frames_out.append(img.get_frame())

    print(f'Skipped {removed} images because of neg shift')
    write(out_file, frames_out)


path = "/mnt/ssd/python_imageprocessing/2x"
out_path = "/mnt/ssd/python_imageprocessing/output"

files = [f for f in listdir(path) if isfile(join(path, f))]

process(files, path, join(out_path, 'final.mp4'))

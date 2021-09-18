import cv2
import numpy as np
import glob
import os
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

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
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

    resized = cv2.resize(image, dim, interpolation = inter)

    return resized


class Image:
    def __init__(self, filename, time=500):
        self.time = time
        self.shifted = 0.0
        self.img = cv2.imread(filename)
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
        self.shifted += self.delta_shift
        if self.shifted > self.shift:
            self.shifted = self.shift
        if self.shifted < 0:
            self.shifted = 0
        return roi


def process(files_to_process, out_file):
    images = []
    frames_out = []

    for filename in files_to_process:
        print(filename)

        img = Image(filename)

        images.append(img)

    prev_image = images[random.randrange(0, len(images))]
    prev_image.reset()

    for img in images:
        img.reset()

        for i in range(50):
            alpha = i/50
            beta = 1.0 - alpha
            dst = cv2.addWeighted(img.get_frame(), alpha, prev_image.get_frame(), beta, 0.0)

            frames_out.append(dst)

        prev_image = img
        for _ in range(100):
            frames_out.append(img.get_frame())
    
    write(out_file, frames_out)


path = "/mnt/ssd/python_imageprocessing/2x"
out_path = "/mnt/ssd/python_imageprocessing/output"

files = [f for f in listdir(path) if isfile(join(path, f))]

process(files, join(out_path, 'hd_try.mp4'))

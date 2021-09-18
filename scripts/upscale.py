#!/usr/bin/env python3

from os import listdir
from os.path import join, isfile
import cv2
from cv2 import dnn_superres
from multiprocessing import Pool

path = "/mnt/ssd/python_imageprocessing/2x"
output = "/mnt/ssd/python_imageprocessing/4x"
model_path = "/mnt/ssd/python_imageprocessing/model/ESPCN_x2.pb"

files = [f for f in listdir(path) if isfile(join(path, f))]

sr = dnn_superres.DnnSuperResImpl_create()
sr.readModel(model_path)
sr.setModel("espcn", 2)


def upscale(in_file):
    img = cv2.imread(join(path, in_file))
    result = sr.upsample(img)
    cv2.imwrite(join(output, in_file), result)


if __name__ == '__main__':
    pool = Pool(4)
    pool.map(upscale, files)

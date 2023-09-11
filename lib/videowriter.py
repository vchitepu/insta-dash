import cv2
import os
import numpy as np
import glob

class VideoWriter:

    def __init__(self, dir: str):
        self.dir = dir

    def generate_video(self):
        img_arr = []
        for f in glob.glob('images/'+self.dir + '/*.jpg'):
            img = cv2.imread(f)
            h, w, l = img.shape
            size = (w,h)
            img_arr.append(img)

        out = cv2.VideoWriter('images/'+self.dir+'.avi', cv2.VideoWriter_fourcc(*'DIVX'), 0.5, size)
        for i in range(len(img_arr)):
            out.write(img_arr[i])
        out.release()

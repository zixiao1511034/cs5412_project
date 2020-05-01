import cv2 as cv
import numpy as np
import glob

img_array = []

for ext in ['*.jpg']:
    for filename in glob.glob('../test_image/'+ext)[::-1]:
        print(filename)
        img = cv.imread(filename)
        # height, width, layers = img.shape
        # size = (width,height)
        # print(size)
        img_array.append(img)

print(len(img_array))
out = cv.VideoWriter('mix_video.avi',cv.VideoWriter_fourcc(*'DIVX'), 3, (1486, 1230))
 
for i in range(len(img_array)):
    if (img.shape[0], img.shape[1]) != (1486, 1230):
        out.write(cv.resize(img_array[i], (1486, 1230)))
    out.write(img_array[i])
out.release()
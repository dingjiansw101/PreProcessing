import numpy as np
import cv2

img = cv2.imread('sydney.jpg');
print(type(img))

cv2.imshow('origin', img)
cv2.imshow('sydney', img[1:1000, 1:100]);


cv2.waitKey();
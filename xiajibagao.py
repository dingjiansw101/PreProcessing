import cv2
import numpy as np
import matplotlib.pyplot as plt
imgname = r'E:\20170719\GF2_PMS1_E23.4_N37.9_20160821_L1A0001776593\GF2_PMS1_E23.4_N37.9_20160821_L1A0001776593-MSS1.tiff'
img1 = cv2.imread(imgname)/4

cv2.imwrite(r'E:\20170719-img8\GF2_PMS1_E23.4_N37.9_20160821_L1A0001776593-MSS1.tiff', img1)
print('shape: ', np.shape(img1))
cv2.imshow('img1', img1[0:400, 0:400])
plt.imshow(img1)
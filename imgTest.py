import cv2
import sys

img_png = cv2.imread(r'C:\Users\dingjian\Desktop\gt.png')
img_jpg = cv2.imread(r'C:\Users\dingjian\Desktop\gt2.jpg')

cv2.imshow(r'img_png', img_png)
print('png size:', sys.getsizeof(img_png))
cv2.imshow(r'img_jpg', img_jpg)
print('jpg size:', sys.getsizeof(img_jpg))
diff = img_png - img_jpg
cv2.imshow(r'diff', diff)
img_tif = cv2.imread(r'C:\Users\dingjian\Desktop\gt3.tif')
print('tif size:', sys.getsizeof(img_tif))
cv2.waitKey()
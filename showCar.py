import cv2

baseimg = 'G:\Data\中科院大学高清航拍目标数据集合\中科院大学高清航拍目标数据集合\PLANE'
basetxt = 'G:\Data\中科院大学高清航拍目标数据集合\中科院大学高清航拍目标数据集合\planeRec'
index = 'P0002'
imgdir = baseimg + '\\' + index + '.png'
imgtxt = basetxt + '\\' + index + '.txt'

imgdir = 'P0002.png'
img = cv2.imread(imgdir)

f = open(imgtxt, 'r')
count = 0
while True:
    count = count + 1
    line = f.readline()
    if line:
        print(line)
        line = line.strip()
        linelist = line.split(' ')
        for index, item in enumerate(linelist):
            linelist[index] = int(float(item))
        x1 = linelist[1] - int(linelist[3]/2)
        x2 = linelist[2] - int(linelist[4]/2)
        x3 = x1 + linelist[3]
        x4 = x2 + linelist[4]
        cv2.rectangle(img, (x1, x2), (x3, x4), (255,0,0))
        print("tuple ", x1, x2, x3, x4)
    else:
        break
print('count:', count)
cv2.imshow('img', img)
cv2.waitKey()
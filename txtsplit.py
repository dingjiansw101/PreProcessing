import os
import codecs
import numpy as np
import math
import tensorflow as tf
from GetFileFromDir import GetFileFromThisRootDir
import argparse
import cv2

class object:
    bbox = np.zeros(8) - 1;
    label = '';
    hardflag = -2;

parser = argparse.ArgumentParser()
parser.add_argument('--dir', default=r'/home/ding/data/GFJL/trainval', type=str)
parser.add_argument('--splitdir', default=r'/home/ding/data/GFJL/trainsplitdir', type=str)
parser.add_argument('--gap', default=10, type=int)
parser.add_argument('--subsize', default=608, type=int)
args = parser.parse_args()
labeldir = os.path.join(args.dir, 'labelTxt')
imagedir = os.path.join(args.dir, 'images')
splitlabeldir = os.path.join(args.splitdir, 'labelTxt')
splitimagedir = os.path.join(args.splitdir, 'images')

print('labeldir', labeldir)
print('imgdir', imagedir)
print('splitlabeldir', splitlabeldir)
print('splitimagedir', splitimagedir)
def txtsplit(imagesize, name, gap, subsize):
    print('imagesize', imagesize)
    grid_m = (int(imagesize[0]))/(subsize - gap)
    grid_n = (int(imagesize[1]))/(subsize - gap)
    filelist = []
    # print('gap', gap)
    # print('type', type(gap))
    # print('subsize', subsize)
    # print('type imagesize', type(subsize))
    # print('imagesize', imagesize[1])
    # print('type imagesize', type(imagesize[1]))
    # print('grid_m', grid_m)
    # print('type grid_m', type(grid_m))
    grid_m = math.floor(grid_m)
    grid_n = math.floor(grid_n)
    for y in range(grid_m):
        filelist.append([])
        for x in range(grid_n):
            subfilename = name + '-' + str(y) + '_' + str(x) + '.txt'
            print('splitlabeldir', splitlabeldir)
            print('subfilename', subfilename)
            subdir = os.path.join(splitlabeldir, subfilename)
            print('txtsubdir', subdir)
            out = codecs.open(subdir, 'w', 'utf_16');
            filelist[y].append(out)
    print('filelist', filelist)
    print('filelist y', len(filelist))
    print('filelist x', len(filelist[0]))
    gtdir = os.path.join(labeldir, name + '.txt')
    f = open(gtdir, 'r', encoding='utf_16')
    print('imagesize: ', imagesize)
    while True:
        line = f.readline()
        if line:
            line = line.strip()
            linelist = line.split(' ')
            tmp = object()
            for index, item in enumerate(tmp.bbox):
                tmp.bbox[index] = int(linelist[index])

            if len(linelist) == 10:
                tmp.hardflag = 1
            else:
                tmp.hardflag = 0;
            if (len(linelist) >= 9):
                tmp.label = linelist[8]
            x1, y1 = tmp.bbox[0], tmp.bbox[1]
            print('x1', x1)
            print('y1', y1)
            stride_x1 = math.floor(x1/(subsize - gap))
            stride_y1 = math.floor(y1/(subsize - gap))
            rightdown_x, rightdown_y = 0, 0
            if (stride_x1 == grid_n):
                stride_x1 = grid_n - 1
                rightdown_x = imagesize[1]
            if (stride_y1 == grid_m):
                stride_y1 = grid_m - 1
                rightdown_y = imagesize[0]

            x3, y3 = tmp.bbox[6], tmp.bbox[7]

            leftup_x = math.floor(stride_x1*(subsize - gap))
            leftup_y = math.floor(stride_y1*(subsize - gap))

            rightdown_x = max(rightdown_x, leftup_x + subsize)
            rightdown_y = max(rightdown_y, leftup_y + subsize)

            if ( (x3 < rightdown_x) and (y3 < rightdown_y) ):
                for i in range(4):
                    tmp.bbox[i*2] = int(tmp.bbox[i*2] - leftup_x)
                for i in range(4):
                    tmp.bbox[1 + i*2] = int(tmp.bbox[1 + i*2] - leftup_y)

                outline = ''
                print('writing')
                for item in tmp.bbox:
                    outline = outline + str(int(item)) + ' '
                if (tmp.label != ''):
                    outline = outline + tmp.label + ' '
                if (tmp.hardflag):
                    outline = outline + str(1)
                print('stride_y', stride_y1)
                print('stride_x', stride_x1)
                filelist[stride_y1][stride_x1].write(outline + '\n')
        else:
            break
    f.close()

def imagesplit(img, imagesize, imgdir, gap, subsize):
    grid_m = (int(imagesize[0]))/(subsize - gap)
    grid_n = (int(imagesize[1]))/(subsize - gap)
    grid_m = math.floor(grid_m)
    grid_n = math.floor(grid_n)

    imgname = os.path.basename(imgdir)
    suffix = os.path.splitext(imgname)[1]
    name = imgname[0:(len(imgname) - len(suffix))];
    print('----------------------start')
    for y in range(grid_m):
        for x in range(grid_n):
            index_x1 = (subsize - gap)*x
            index_x2 = index_x1 + subsize
            index_y1 = (subsize - gap)*y
            index_y2 = index_y1 + subsize

            if (x == grid_n - 1):
                index_x2 = imagesize[1]
            if (y == grid_m - 1):
                index_y2 = imagesize[0]
            print('index_x1', index_x1)
            print('index_x2', index_x2)
            print('index_y1', index_y1)
            print('index_y2', index_y2)
            subimg = img[index_y1:index_y2,
                     index_x1:index_x2]
            print('subimg shape', np.shape(subimg))
            subname = name + '-' + str(y) + '_' + str(x) + suffix
            print('suffix', suffix)
            subdir = os.path.join(splitimagedir, subname)
            print('imgsubdir', subdir)
            cv2.imwrite(subdir, subimg)
    print('<<<<<<<<<<<<<<<<<<<<<<end')

def splitdata(imgdir, gap, subsize):
    img = cv2.imread(imgdir)
    imagesize = img.shape


    imgname = os.path.basename(imgdir)
    suffix = os.path.splitext(imgname)[1]
    name = imgname[0:(len(imgname) - len(suffix))];
    print('imgname', imgname)
    print('name', name)
    txtsplit(imagesize, name, gap, subsize)
    imagesplit(img, imagesize, imgdir, gap, subsize)


def main():

    imagelist = GetFileFromThisRootDir(imagedir);
    count = 0
    for imgname in imagelist:
        print('count: ', count)
        count = count + 1
        print(imgname)
        splitdata(imgname, args.gap, args.subsize)

if __name__ == '__main__':
    main()
def txtsplit2(txt, basedir):
    print('txt', txt)
    f = open(txt, 'r', encoding='utf_16')
    strlist = txt.split('\\');
    filename = strlist[len(strlist) - 1]
    suffix = os.path.splitext(filename)[1]
    filename = filename[0:(len(filename) - len(suffix))];
    #dir = basedir + str + '.txt';
    #os.mkdir(basedir)

    ##open all the split txt, assume it is divided into 4*4
    filelist = []
    for y in range(4):
        filelist.append([])
        for x in range(4):
            dir = basedir + filename + '_' + str(y + 1) + '_' + str(x + 1) + '.txt'
            out = codecs.open(dir, 'w', 'utf_16');
            filelist[y].append(out)
    print('filelist', filelist)

    cnt = 0;
    allcnt = 0;
    print(txt)
    while True:
        allcnt = allcnt + 1;
        print("allcnt", allcnt);
        cnt = cnt + 1;
        line = f.readline();
        if line:
            print(line)
            line = line.strip()
            linelist = line.split(' ');
            print(linelist);
            tmp = object()
            for index, item in enumerate(tmp.bbox):
                tmp.bbox[index] = int(linelist[index])

            if len(linelist) == 10:
                tmp.hardflag = 1
            else:
                tmp.hardflag = 0;
            if (len(linelist) >= 9):
                tmp.label = int(linelist[8])
            ###determine the box belong to which patch
            stride_x = tmp.bbox[0]/4000 + 1
            stride_y = tmp.bbox[1]/4000 + 1
            if (stride_x > 4):
                stride_x = 4
            if (stride_y > 4):
                stride_y = 4
            stride_x = math.floor(stride_x)
            stride_y = math.floor(stride_y)
            flag = True
            print('stride_x', stride_x, 'stride_y', stride_y)
            for i in range(3):
                tmp_x = tmp.bbox[2 + i*2]/4000 + 1
                tmp_y = tmp.bbox[2 + i*2 + 1]/4000 + 1
                if (tmp_x > 4):
                    tmp_x = 4
                if (tmp_y > 4):
                    tmp_y = 4
                tmp_x = math.floor(tmp_x)
                tmp_y = math.floor(tmp_y)
                print('tmp_x', tmp_x, 'tmp_y', tmp_y)
                if (stride_x != tmp_x) or (stride_y != tmp_y) :
                    flag = False
                    break
            if flag:
                for i in range(4):
                    tmp.bbox[i*2] = int(tmp.bbox[i*2] - 4000*(stride_x-1))
                for i in range(4):
                    tmp.bbox[1 + i*2] = int(tmp.bbox[1 + i*2] - 4000*(stride_y - 1))

                outline = ''
                print('writing')
                for item in tmp.bbox:
                    outline = outline + str(int(item)) + ' '
                if (tmp.label != -1):
                    outline = outline + str(tmp.label) + ' '
                if (tmp.hardflag):
                    outline = outline + str(1)
                filelist[stride_y - 1][stride_x - 1].write(outline + '\n')
                #out.write(line + '\n');
        else:
            break;
    f.close()
#txt = 'G:\oldtonew\oldtxt\JL101A_PMS_20160518022947_000008798_202_0011_001_L1_PAN.txt'
#dir = 'G:\oldtonew\\newtxt\\'
#txtsplit(txt, dir)
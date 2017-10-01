#coding:utf-8
import os
import argparse
import utils as util
import shutil
import cv2
import numpy as np
import codecs
import

basepath = r'E:\GoogleEarth\up-9-25-data\secondjpg'
paths = []
paths.append(os.path.join(basepath, 'information'))
paths.append(os.path.join(basepath, 'images'))
paths.append(os.path.join(basepath, 'labelTxt'))
def filerm():
    rmfiles = util.filesetcalc(paths[1], paths[2], 'd')
    for rmname in rmfiles:
        rmdir = os.path.join(paths[1], rmname + '.tif')
        print('rmdir:', rmdir)
        os.remove(rmdir)
def filemove():
    movepath = r'E:\GoogleEarth\up-9-10\tangjun\unLimages'
    srcfiles = util.filesetcalc(paths[1], paths[0], 'd')
    #print('rmfiles:', rmfiles)

    for name in srcfiles:
        srcdir = os.path.join(paths[1], name + '.tif')
        dstdir = os.path.join(movepath, name + '.tif')
        print('dstdir:', dstdir)
        shutil.move(srcdir, dstdir)
def addDate(date):
    #date = '_7-30'
    for path in paths:
        filelist = util.GetFileFromThisRootDir(path)
        for dir in filelist:
            name = os.path.splitext(dir)[0]
            suffix = os.path.splitext(dir)[1]
            newname = name + date + suffix
            print('oldname:', dir)
            print('newname:', newname)
            os.rename(dir, newname)
def rmDate(date):
    #date = r'_7-29'
    for path in paths:
        filelist = util.GetFileFromThisRootDir(path)
        for dir in filelist:
            #name = os.path.splitext(dir)[0]
            #suffix = os.path.splitext(dir)[1]
            newname = dir.replace(date, '')
            print('oldname:', dir)
            print('newname:', newname)
            os.rename(dir, newname)
def checkA():
    inter_set = util.filesetcalc(paths[0], paths[1], 'i')
    print('inter_se:', inter_set)
    count = 0
    out_file = os.path.join(basepath, 'autocheck', 'check.txt')
    f_out = open(out_file, 'w')
    for name in inter_set:
        imagename = os.path.join(paths[1], name + '.tif')
        infoname = os.path.join(paths[0], name + '.txt')
        f = open(infoname, 'r')
        lines = f.readlines()
        w_info = lines[0].split('：')[-1]
        h_info = lines[1].split('：')[-1]
        print('imagname:', imagename)
        image = cv2.imread(imagename)
        print('shape:', np.shape(image))
        print('tuple:', (int(h_info), int(w_info)))
        if ((int(h_info), int(w_info)) != np.shape(image)[0:2]):
            print('name:', name)
            f_out.write(name + '\n')
            count = count + 1
        print('count:', count)
    f_out.write(str(count))
def checkB():
    filelist = util.GetFileFromThisRootDir(paths[0])
    imagesizes = {}
    for file in filelist:
        f = open(file)
        lines = f.readlines()
        w_info = lines[0].split('：')[-1]
        h_info = lines[1].split('：')[-1]
        imagesizes[file] = (int(w_info), int(h_info))
    duplicates = [x for x in imagesizes.keys() if list(imagesizes.values()).count(imagesizes[x]) > 1]
    print('duplicates:', duplicates)
    out_file = os.path.join(basepath, 'duplicates', 'duplicates.txt')
    outpath = os.path.join(basepath, 'duplicates')
    f_out = open(out_file, 'w')
    for dir in duplicates:
        f_out.write(dir + '\n')
        name = os.path.splitext(os.path.basename(dir))[0]
        imgname = name + '.tif'
        oldname = os.path.join(paths[1], imgname)
        newname = os.path.join(outpath, imgname)
        print('oldname:',oldname)
        print('newname:', newname)
        shutil.copyfile(oldname, newname)
def parseDarknetOut():
    file = r'E:\yanshen\dataset2\GFJLchips\GFJLtestchips\comp4_det_test_plane.txt'
    outpath = r'E:\yanshen\dataset2\GFJLchips\GFJLtestchips\resultsTxt'
    f = open(file, 'r')
    lines = f.readlines()
    splitlines = [x.strip().split(' ') for x in lines]
    filelists = {}
    count = 0
    for index, bbox in enumerate(splitlines):
            print('index:', index)
            print('name1:', bbox[0])
            name = bbox[0][0: -4]
            if name not in filelists:
                filedir = os.path.join(outpath, name + '.txt')
                filelists[name] = codecs.open(filedir, 'w', 'utf_16')
            stride_y = int(bbox[0][-3])
            stride_x = int(bbox[0][-1])
            print('name:', name)
            print('stride_y:', stride_y)
            print('stride_x:', stride_x)
            outlist = []
            x = np.zeros(4)
            y = np.zeros(4)
            xmin = float(bbox[2])
            ymin = float(bbox[3])
            xmax = float(bbox[4])
            ymax = float(bbox[5])

            x[0], y[0] = xmin, ymin
            x[1], y[1] = xmax, ymin
            x[2], y[2] = xmax, ymax
            x[3], y[3] = xmin, ymax


            for i in range(4):
                outlist.append((stride_x) * 598 + x[i])
                outlist.append((stride_y) * 598 + y[i])
            ## '9' is not the plane id, just use the coloer of '9':green
            outlist.append(9)
            for index, item in enumerate(outlist):
                outlist[index] = str(item)
            outline = ' '.join(outlist)
            print(outline)
            filelists[name].write(outline + '\n')
            if (name == 'GF2_PMS1_E114.0_N22.3_20161010_L1A0001879601-PAN1_2_3'):
                count = count + 1
            print('count:', count)
def findDiff():
    path = r'E:\GoogleEarth\up-9-25-data\secondjpg\train\images'
    splitpath = r'E:\GoogleEarth\up-9-25-data\secondjpg\trainsplit\images'
    imglist = util.GetFileFromThisRootDir(path)
    splitimglist = util.GetFileFromThisRootDir(splitpath)
    imgnames = {os.path.basename(os.path.splitext(x)[0]) for x in imglist}
    splitnames = {os.path.basename(os.path.splitext(x)[0])[0: -4] for x in splitimglist}
    print('imgnames;', imgnames)
    print('splitnames:', splitnames)
    diff1 = imgnames.difference(splitnames)
    print('diff:', diff1)

if __name__ == '__main__':
    #checkB()
    pass
    #parseDarknetOut()
    #filerm()
    #rmDate()
    #addDate('_8-9')
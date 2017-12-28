#coding:utf-8
from __future__ import print_function
import os
import argparse
import utils as util
import shutil
import cv2
import numpy as np
import codecs
import sys
import re
import random

basepath = r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\zhaochaonan'
paths = []
paths.append(os.path.join(basepath, 'information'))
paths.append(os.path.join(basepath, 'images'))
paths.append(os.path.join(basepath, 'labelTxt'))
paths.append(os.path.join(basepath, 'jpgs'))
def filerm2(path2, extent):
    path1 = r'/home/dj/data/bod/labels'
    rmfiles = util.filesetcalc(path2, path1, 'd')
    for rmname in rmfiles:
        rmdir = os.path.join(path2, rmname + extent)
        print('rmdir:', rmdir)
        os.remove(rmdir)
def filerm(path1, path2, extent):
    rmfiles = util.filesetcalc(path1, path2, 'd')
    for rmname in rmfiles:
        rmdir = os.path.join(path1, rmname + extent)
        print('rmdir:', rmdir)
        os.remove(rmdir)

def filerm3():
    filerm(r'E:\bod-dataset\wordlabel',
           r'E:\bod-dataset\images',
           '.txt')
def batchfilerm():
    rmpath = []
    basepath = r'/home/dj/data/bod'
    rmpath.append(os.path.join(basepath, 'testsplit', 'images'))
    rmpath.append(os.path.join(basepath, 'testsplit', 'labelTxt'))
    rmpath.append(os.path.join(basepath, 'trainsplit-2', 'images'))
    rmpath.append(os.path.join(basepath, 'trainsplit-2', 'labelTxt'))
    filerm2(rmpath[0], '.jpg')
    filerm2(rmpath[1], '.txt')
    filerm2(rmpath[2], '.jpg')
    filerm2(rmpath[3], '.txt')
def extractmark():
    basepath = r'E:\GoogleEarth\up-9-25-data\secondjpg\test'
    markpath = os.path.join(basepath, r'mark')
    labelpath = os.path.join(basepath, r'labelTxt')
    imgpath = os.path.join(basepath, r'images')
    reannotationpath = os.path.join(basepath, r'reannotation')
    marklist = util.GetFileFromThisRootDir(markpath)
    marknames = [util.mybasename(x[0:-9]) for x in marklist]
    labellists = util.GetFileFromThisRootDir(labelpath)
    for fullname in labellists:
        imgname = util.mybasename(fullname)
        if imgname in marknames:
            srcimgname = os.path.join(imgpath, imgname + '.tif')
            dstimgname = os.path.join(reannotationpath, 'images', imgname + '.tif')
            srclabelTxt = os.path.join(labelpath, imgname + '.txt')
            dstlabelTxt = os.path.join(reannotationpath, 'labelTxt', imgname + '.txt')
            shutil.move(srcimgname, dstimgname)
            shutil.move(srclabelTxt, dstlabelTxt)

def filemove(srcpath, dstpath, filenames, extent):
    for name in filenames:
        srcdir = os.path.join(srcpath, name + extent)
        dstdir = os.path.join(dstpath, name + extent)
        print('srcdir:', srcdir)
        print('dstdir:', dstdir)
        if os.path.exists(srcdir):
            shutil.move(srcdir, dstdir)

def filecopy(srcpath, dstpath, filenames, extent):
    for name in filenames:
        srcdir = os.path.join(srcpath, name + extent)
        dstdir = os.path.join(dstpath, name + extent)
        print('srcdir:', srcdir)
        print('dstdir:', dstdir)
        if os.path.exists(srcdir):
            shutil.copyfile(srcdir, dstdir)
def filemove3():
    basepath = r'E:\GoogleEarth\up-9-25-data\SecondQuality\zhaochaonan'
    f = open(os.path.join(basepath, 'movelist.txt'), 'r')
    lines = f.readlines()
    filenames = [util.mybasename(x.strip()) for x in lines]
    imgsrcpath = os.path.join(basepath, 'images')
    imgdstpath = os.path.join(basepath, 'discard', 'images')
    txtsrcpath = os.path.join(basepath, 'labelTxt')
    txtdstpath = os.path.join(basepath, 'discard', 'labelTxt')
    filemove(imgsrcpath,imgdstpath, filenames, '.tif')
    filemove(txtsrcpath, txtdstpath, filenames, '.txt')
def filemove5():
    filenames = util.filesetcalc(paths[1], paths[2], 'd')
    filemove(r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\images',
             r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\discard\images',
             filenames,
             '.jpg')

def filemove4():
    path1 = r'E:\GoogleEarth\up-9-25-data\SecondQuality\leiyaxian\all\labelTxt'
    path2 = r'E:\GoogleEarth\up-9-25-data\SecondQuality\leiyaxian\all\images'
    filenames = util.filesetcalc(path1, path2, 'd')
    dstpath = r'E:\GoogleEarth\up-9-25-data\SecondQuality\leiyaxian\all\nonobjectset\labelTxt'
    filemove(path1, dstpath, filenames, '.txt')
def filecopy5():
    imgdst = r'E:\downloaddataset\HRSC2016\HRSC2016\HRSC2016\HRSC2016\Train\AllImages'
    annodst = r'E:\downloaddataset\HRSC2016\HRSC2016\HRSC2016\HRSC2016\Train\Annotations'
    annosrc = r'E:\downloaddataset\HRSC2016\HRSC2016\HRSC2016\HRSC2016\FullDataSet\Annotations'
    filenames = util.GetFileFromThisRootDir(imgdst)
    names = [util.mybasename(x.strip()) for x in filenames]
    filecopy(annosrc, annodst, names, '.xml')
# def filemove3():
#     f = open(r'E:\GoogleEarth\up-9-25-data\SecondQuality\leiyaxian\all\movelist.txt', 'r')
#     lines = f.readlines()
#     filenames = [util.mybasename(x.strip()) for x in lines]
#     srcpathimg = r'E:\GoogleEarth\up-9-25-data\SecondQuality\leiyaxian\all\images'
#     dstpathimg = r'E:\GoogleEarth\up-9-25-data\SecondQuality\leiyaxian\all\nonobjectset\images'
#     filemove(srcpathimg, dstpathimg, filenames, '.tif')
#     srcpathlabel = r'E:\GoogleEarth\up-9-25-data\SecondQuality\leiyaxian\all\labelTxt'
#     dstpathlabel = r'E:\GoogleEarth\up-9-25-data\SecondQuality\leiyaxian\all\nonobjectset\labelTxt'
#     filemove(srcpathlabel, dstpathlabel, filenames, '.txt')
def filemove2():
    movepath = r'E:\GoogleEarth\up-9-25-data\SecondQuality\jianwenyun\carship'
    markpath = os.path.join(basepath, 'mark')
    filelist = util.GetFileFromThisRootDir(markpath, '.txt')
    srcfiles = [os.path.basename(x)[0:-9] for x in filelist]
    filemove(basepath, movepath, srcfiles)
class nonobjectFinder():
    def __init__(self,
                 basepath,
                 mode):
        ## for mode bod
        self.mode = mode
        self.basepath = basepath
        assert (self.mode == 'bod') or (self.mode == 'dark'), 'mode must be bod or dark'
        if self.mode == 'dark':
            self.gtpath = os.path.join(basepath, 'labels')
            self.imgpath = os.path.join(basepath, 'JPEGImages')
        else:
            self.gtpath = os.path.join(basepath, 'labelTxt')
            self.imgpath = os.path.join(basepath, 'images')
    def assertempty(self):
        self.nonobjectfind(self.assert_op)
    def move_op(self, filename):
        dstbasepath = os.path.join(self.basepath, r'nonobjectset')
        dstimgpath = os.path.join(dstbasepath, 'images')
        dstlabelpath = os.path.join(dstbasepath, 'labelTxt')
        if self.mode == 'dark':
            ## TODO: finish the code
            pass
            #srcdir = os.path.join(self, filename)
            #dstdir = os.path.join(dstpath, filename)
        else:
            imgsrcdir = os.path.join(self.imgpath, filename + '.png')
            imgdstdir = os.path.join(dstimgpath, filename + '.png')
            txtsrcdir = os.path.join(self.gtpath, filename + '.txt')
            txtdstdir = os.path.join(dstlabelpath, filename + '.txt')
            print(imgsrcdir)
            print(txtdstdir)
            shutil.move(imgsrcdir, imgdstdir)
            shutil.move(txtsrcdir, txtdstdir)
    def assert_op(self, filename):
            assert 0, filename + ' ' + 'is empty'
    def nonobjectfind(self, op):
        filelist = util.GetFileFromThisRootDir(self.gtpath)
        for filename in filelist:
            if self.mode == 'bod':
                if (sys.version_info >= (3, 5)):
                    f = open(filename, 'r', encoding='utf-16')
                else:
                    f = codecs.open(filename, 'r', 'utf_16')
            elif self.mode == 'dark':
                f = open(filename, 'r')
            lines = f.readlines()
            f.close()
            print('filename:', filename)
            basename = os.path.basename(os.path.splitext(filename)[0])
            if (len(lines) == 0):
                op(basename)
    def nonobjectfilemove(self):
        ## TODO: finish the code
        #pass
        if self.mode == 'bod':
            self.nonobjectfind(self.move_op)
    def rm_op(self, filename):
        print('rmfilename:', filename)

        os.remove(os.path.join(self.gtpath, filename + '.txt'))
        os.remove(os.path.join(self.imgpath, filename + '.jpg'))
    def nonobjectfilerm(self):
        self.nonobjectfind(self.rm_op)

    def filemove3(self):
        testtxtdir = r'E:\GoogleEarth\up-9-25-data\secondjpg\testsplit\test.txt'
        f = open(testtxtdir, 'r')
        lines = f.readlines()
        print('len(lines):', len(lines))
        splitlines = [x.strip() for x in lines]
        labelset = set(util.GetFileFromThisRootDir(r'E:\GoogleEarth\up-9-25-data\secondjpg\testsplit\labelTxt'))
        labelset = { os.path.basename(os.path.splitext(x.strip())[0]) for x in labelset}
        print('len(splitlines):', len(splitlines))
        diffset = labelset.difference(splitlines)
        for name in diffset:
            #print('name:', name)
            self.move_op(name)
def extractfilename():
    dir = r'E:\GoogleEarth\up-9-25-data\secondjpg\test\bod_test.txt'
    outdir = r'E:\GoogleEarth\up-9-25-data\secondjpg\test\test.txt'
    f = open(dir, 'r')
    lines = f.readlines()
    f_out = open(outdir, 'w')
    for line in lines:
        name = os.path.splitext(os.path.basename(line.strip()))[0]
        f_out.write(name + '\n')
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
def movesuffix(inputpath, outpath):
    filelist = util.GetFileFromThisRootDir(inputpath)
    inversedic = util.keyvalueReverse(util.datamap2)
    for fullname in filelist:
        name = os.path.basename(os.path.splitext(fullname)[0])
        f = open(fullname, 'r')
        lines = f.readlines()
        outname = os.path.join(outpath, 'comp4_det_test_' + inversedic[name[15:]] + '.txt')
        f_out = open(outname, 'w')
        for line in lines:
            splitline = line.strip().split(' ')
            splitline[0] = os.path.splitext(splitline[0])[0]
            #print('splitline:', splitline)
            f_out.write(' '.join(splitline) + '\n')

def rename():
    path = r'E:\GFJL\gaofen2\labelmovedotTxt'
    path2 = r'E:\GFJL\gaofen2\out'
    filelist = util.GetFileFromThisRootDir(path)
    print('len:', len(filelist))
    for fullname in filelist:
        basename = util.mybasename(fullname)
        splitname = basename.split('PAN')
        position = splitname[-1]
        numbers = re.findall(r'\d+', position)
        print(numbers)
        newname = splitname[0] + 'PAN' + numbers[0] + '_' + numbers[1] + '_' + numbers[2] + '.txt'
        print('olddir:', fullname)
        #newdir = os.path.join(path, newname)
        newdir = os.path.join(path2, newname)
        print('newdir:', newdir)
        shutil.copyfile(fullname, newdir)

## TODO: abstract rename: rename consist of path, regular

def rename2():
    path = r'E:\downloaddataset\CarPlane\PLANE'
    outpath = r'E:\downloaddataset\CarPlane\results\images'
    imglist = util.GetFileFromThisRootDir(path, '.png')
    for imgname in imglist:
        oldname = util.mybasename(imgname)
        num = re.findall('\d+', oldname)[0]
        num = int(num)
        newnum = str(num + 510)
        newname = 'P' + newnum.zfill(4) + '.png'
        dstname = os.path.join(outpath, newname)
        shutil.copyfile(imgname, dstname)
def GetSetList(base_basepath, splitset):
    basepath = os.path.join(base_basepath, splitset)
    gtpath = os.path.join(basepath, 'wordlabel')
    fullnames = util.GetFileFromThisRootDir(gtpath)
    names = {util.mybasename(x) for x in fullnames}
    outname = os.path.join(basepath, splitset + '.txt')
    with open(outname, 'w') as f_out:
        for name in names:
            f_out.write(name + '\n')
def GetSetList(splitset):
    basepath = os.path.join(r'E:\bod-dataset', splitset)
    gtpath = os.path.join(basepath, 'wordlabel')
    fullnames = util.GetFileFromThisRootDir(gtpath)
    names = {util.mybasename(x) for x in fullnames}
    outname = os.path.join(basepath, splitset + '.txt')
    with open(outname, 'w') as f_out:
        for name in names:
            f_out.write(name + '\n')

def testGetSetList():
    GetSetList('testset')
    GetSetList('trainset')
    GetSetList('valset')

# for darknet
def GetTrainList(basepath):

    #labelpath = os.path.join(basepath, 'labels')
    imgpath  = os.path.join(basepath, 'JPEGImages')
    splitlist = util.GetFileFromThisRootDir(imgpath)
    splitlinames = [util.mybasename(x) for x in splitlist]
    trainset = util.GetListFromfile(os.path.join(basepath, 'trainset.txt'))
    testset = util.GetListFromfile(os.path.join(basepath, 'testset.txt'))
    valset = util.GetListFromfile(os.path.join(basepath, 'valset.txt'))

    trainvalset = trainset.union(valset)
    train_f = open(os.path.join(basepath, 'train.txt'), 'w')
    test_f  = open(os.path.join(basepath, 'test.txt'), 'w')
    for splitname in splitlinames:
        initialname = util.extractInitailName(splitname)
        if initialname in trainvalset:
            train_f.write(os.path.join(imgpath, splitname + '.jpg') + '\n')
        elif initialname in testset:
            test_f.write(os.path.join(imgpath, splitname + '.jpg') + '\n')
    train_f.close()
    test_f.close()

def movejpgsuffix(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for fullname in filelist:
        f = open(fullname, 'r')
        lines = f.readlines()
        splitlines = [x.strip().split(' ') for x in lines]
        outlines = [(util.mybasename(x[0]) + ' ' + ' '.join(x[1:])) for x in splitlines]
#         outlines = [(util.mybasename(x[0]) + ' ' + ' '.join(x[1:])) for x in splitlines
#                     if ((float(x[3]) - float(x[1] ) ) * (float(x[4]) - float(x[2] ) ) ) > (15 * 15)]
        print(outlines)
        name = util.mybasename(fullname)
        outname = os.path.join(dstpath, name + '.txt')
        with open(outname, 'w') as f_out:

            for index, outline in enumerate(outlines):
                if index == (len(outlines) - 1):
                    f_out.write(outline)
                else:
                    f_out.write(outline + '\n')

def ExtractSubCategory():
    basepath = r'E:\bod-dataset\patches'
    classdict = util.getcategory(
            basepath,
            r'wordlabel',
            )
    extractclass = ['helicopter', 'bridge', 'baseball-diamond',
                    'ground-track-field', 'baseketball-court',
                    'soccer-ball-field', 'harbor']
    filelist = []
    for extractname in extractclass:
        for filename in classdict[extractname]:
            if filename not in filelist:
                filelist.append(filename)
    filecopy(r'E:\bod-dataset\patches\wordlabel',
             r'E:\bod-dataset\patches\subcategorylabel',
             filelist, '.txt')
def mergemark(path, outdir):
    filelist = util.GetFileFromThisRootDir(path, '.txt')
    outlines = []
    for fullname in filelist:
        f = open(fullname, 'r', encoding='utf_16')
        line = f.readline()
        name = os.path.splitext(os.path.basename(fullname))[0]
        outlines.append(name + ' ' + line)
    f_out = open(outdir, 'w')
    for line in outlines:
        f_out.write(line + '\n')

def TrainTestSplit():
    basepath = r'E:\downloaddataset\NWPU\NWPU'
    filelist = util.GetFileFromThisRootDir(os.path.join(basepath, 'images'))
    name = [os.path.basename(os.path.splitext(x)[0]) for x in filelist if (x != 'Thumbs')]
    train_len = int(len(name) * 0.5)
    test_len = len(name) - train_len
    print('train_len:', train_len)
    print('test_len:', test_len)
    random.shuffle(name)
    print('shuffle name:', name)
    train_set= set(name[0:train_len])
    test_set = set(name[train_len:])
    print('intersection:', train_set.intersection(test_set))
    imgsrcpath = os.path.join(basepath, 'images')
    txtsrcpath = os.path.join(basepath, 'labelTxt')
    imgtestpath = os.path.join(basepath, 'testset', 'images')
    txttestpath = os.path.join(basepath, 'testset', 'labelTxt')
    imgtrainpath = os.path.join(basepath, 'trainset', 'images')
    txttrainpath = os.path.join(basepath, 'trainset', 'labelTxt')

    filemove(imgsrcpath, imgtestpath, test_set, '.jpg')
    filemove(txtsrcpath, txttestpath, test_set, '.txt')
    filemove(imgsrcpath, imgtrainpath, train_set, '.jpg')
    filemove(txtsrcpath, txttrainpath, train_set, '.txt')
def getfiles2singletxt(path, outfilename):
    filelist = util.GetFileFromThisRootDir(path)
    with open(outfilename, 'w') as f_out:
        for fullname in filelist:
            name = util.mybasename(fullname)
            f_out.write(name + '\n')
def nwpugetTrainTestsetTxt():
    getfiles2singletxt(r'E:\downloaddataset\NWPU\NWPU\testset\labelTxt',
                       r'E:\downloaddataset\NWPU\NWPU\testset\testset.txt')
    getfiles2singletxt(r'E:\downloaddataset\NWPU\NWPU\trainset\labelTxt',
                       r'E:\downloaddataset\NWPU\NWPU\trainset\traintset.txt')

def samplespng2jpg():
    filelist = util.GetFileFromThisRootDir(r'E:\documentation\dataset\aerial_detection_dataset\samples', '.png')
    outpath = r'E:\documentation\dataset\aerial_detection_dataset\samplesjpg'
    for fullname in filelist:
        imgname = util.mybasename(fullname)
        outname = os.path.join(outpath, imgname + '.jpg')
        img = cv2.imread(fullname)
        cv2.imwrite(outname, img)

if __name__ == '__main__':
    #checkB()
    #parseDarknetOut()
    #extractfilename()
    #rmDate()
    #addDate('_8-9')
    #testcheckexistempty()
    #nonobjectfind = nonobjectFinder(r'E:\GoogleEarth\up-9-25-data\SecondQuality\leiyaxian\all', 'bod')
    #nonobjectfind.nonobjectfilemove()
    #nonobjectfind.nonobjectfilerm()
    #basepath = r'E:\GoogleEarth\up-9-25-data\secondjpg\results'
    #movesuffix(os.path.join(basepath, 'bod_backup2'), os.path.join(basepath, 'movejpg_bod_backup2'))
#    movejpgsuffix()
    #extractmark()
    #filerm(paths[3], paths[1], '.jpg')
    #find = nonobjectFinder(r'E:\GFJL\JL', 'bod')
    #find.nonobjectfilemove()
    #print(namelist)
    #filemove3()
    #GetTrainList(r'/home/dj/data/bod-v3')
    #testGetSetList()
    #GetTrainList()
    #ExtractSubCategory()
    #basepath = r'/home/dj/data/bod-subset'
    #GetTrainList(basepath)
    #GetTrainList(r'/home/dj/data/bod-v2')

    filerm(r'E:\bod-dataset\jpgs',
           r'E:\bod-dataset\images',
           '.jpg')
    # movejpgsuffix(r'E:\bod-dataset\results\bod_ssd1024_647571',
    #               r'E:\bod-dataset\results\bod_ssd1024_647571-nms')
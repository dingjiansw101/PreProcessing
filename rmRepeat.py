#coding:utf-8
import os
import codecs,sys
import cv2
import string
import re
import math
import argparse
from GetFileFromDir import GetFileFromThisRootDir

def removeRepImg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--testdir', default=r'E:\Data\dataset2\test\images', type=str)
    parser.add_argument('--traindir', default=r'E:\Data\dataset2\trainval\images', type=str)
    args = parser.parse_args()

    testlist = GetFileFromThisRootDir(args.testdir)
    trainlis = GetFileFromThisRootDir(args.traindir)

    testnames = []
    trainnames = []
    for file in testlist:
        strlist = file.split('\\');
        filename = strlist[len(strlist) - 1];
        testnames.append(filename)
    for file in trainlis:
        strlist = file.split('\\');
        filename = strlist[len(strlist) - 1];
        trainnames.append(filename)
    for item in testnames:
        if (item in trainnames):
            dir = os.path.join(args.testdir, item)
            print('dir:', dir)
            os.remove(dir)
def reserRepImgTxt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--testdir', default=r'E:\Data\dataset2\test\images', type=str)
    parser.add_argument('--traindir', default=r'E:\Data\dataset2\test\labelTxt', type=str)
    args = parser.parse_args()

    testlist = GetFileFromThisRootDir(args.testdir)
    trainlist = GetFileFromThisRootDir(args.traindir)

    for testfile in testlist:
        strlist = testfile.split('\\');
        testname = strlist[len(strlist) - 1];
        suffix = os.path.splitext(testname)[1]
        testname = testname[0:(len(testname) - len(suffix))];
        flag = False ## False are to be deleted
        for trainfile in trainlist:
            strlist = trainfile.split('\\');
            trainname = strlist[len(strlist) - 1];
            suffix = os.path.splitext(trainname)[1]
            trainname = trainname[0:(len(trainname) - len(suffix))];
            if (testname == trainname):
                #print('testname', testname)
                #print('trainname', trainname)
                flag = True
                break
        if (flag == False):
            dir = os.path.join(args.testdir, testfile)
            print('dir:', dir)
            #os.remove(dir)

    for trainfile in trainlist:
        strlist = trainfile.split('\\');
        trainname = strlist[len(strlist) - 1];
        suffix = os.path.splitext(trainname)[1]
        trainname = trainname[0:(len(trainname) - len(suffix))];
        flag = False ## False are to be deleted
        for testfile in testlist:
            strlist = testfile.split('\\');
            testname = strlist[len(strlist) - 1];
            suffix = os.path.splitext(testname)[1]
            testname = testname[0:(len(testname) - len(suffix))];
            if (testname == trainname):
                flag = True
                break
        if (flag == False):
            dir = os.path.join(args.traindir, trainfile)
            print('dir:', dir)
            #os.remove(dir)
if __name__ == '__main__':
    reserRepImgTxt()
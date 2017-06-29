#coding:utf-8
import os
import codecs,sys
import cv2
import string
import re
import math
import numpy as np

def GetFileFromThisRootDir(dir,ext = None):
  allfiles = []
  needExtFilter = (ext != None)
  for root,dirs,files in os.walk(dir):
    for filespath in files:
      filepath = os.path.join(root, filespath)
      extension = os.path.splitext(filepath)[1][1:]
      if needExtFilter and extension in ext:
        allfiles.append(filepath)
      elif not needExtFilter:
        allfiles.append(filepath)
  return allfiles

import os;
classname = ['0', '2', '5', '6', '9']

def copyimg():
    path = r"E:\Data\jilin\5labelTxt";
    inpath = "E:\Data\jilin\images";
    outpath = r"E:\Data\jilin\5images";
    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
    for index, files in enumerate(filelist):#遍历所有文件
        Olddir=os.path.join(path,files);#原来的文件路径
        if os.path.isdir(Olddir):#如果是文件夹则跳过
            continue;
        filename=os.path.splitext(files)[0];#文件名
        filetype=os.path.splitext(files)[1];#文件扩展名
        filename = filename + '.tif'
        imgname = os.path.join(inpath, filename)
        print('read img', imgname)
        img = cv2.imread(imgname)
        print('shape', img)
        outname = os.path.join(outpath, filename)
        print('outname', outname)
        print('write img')
        cv2.imwrite(outname, img)

copyimg();
#coding:utf-8
import os
import codecs,sys
import cv2
import string
import re
import math

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

def rename():
    path="E:\Data\jilin\labelTxt";
    outpath = r"E:\Data\jilin\5labelTxt";
    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
    for index, files in enumerate(filelist):#遍历所有文件
        Olddir=os.path.join(path,files);#原来的文件路径
        if os.path.isdir(Olddir):#如果是文件夹则跳过
            continue;
        f = open(Olddir, 'r', encoding='utf_16')
        outname = os.path.join(outpath, files)
        print('filename', files)

        out = codecs.open(outname, 'w', 'utf_16')
        #print('before flag', flag)
        flag = 0
        while True:
            line = f.readline()
            if line:
                line2 = line.strip()
                linelist = line2.split(' ')
                if (linelist[8]  in classname):
                    flag = 1
                    out.write(line)
            else:
                break
        f.close()
        out.close()
        if (flag == 0):
            os.remove(outname)
rename();
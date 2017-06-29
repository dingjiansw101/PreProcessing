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
def rename():
    path="E:\Data\gaofen2\imgs\\test";
    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
    for index, files in enumerate(filelist):#遍历所有文件
        Olddir=os.path.join(path,files);#原来的文件路径
        if os.path.isdir(Olddir):#如果是文件夹则跳过
            continue;
        filename=os.path.splitext(files)[0];#文件名
        filetype=os.path.splitext(files)[1];#文件扩展名
        print('filename', filename)
        print('index', index)
        #newname = str = "{0:0>4}".format(index)
        #newname = newname + '_0.175m'

        ##for move the tif's "."
        newname, number = re.subn(r'\._', r'_', filename)
        print('newname', newname)
        Newdir=os.path.join(path,newname+filetype);#新的文件路径
        os.rename(Olddir,Newdir);#重命名
rename();
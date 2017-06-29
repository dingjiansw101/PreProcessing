#coding:utf-8
import os
import codecs,sys
import cv2
import string
import re
import math
from GetFileFromDir import GetFileFromThisRootDir

import os;
def rename():
    path=r"E:\Data\GF2\Tool\labelTxt";
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
        newfiletype, number2 =re.subn(r'\.', '', filetype)
        #print('filetype', newfiletype)
        Newdir=os.path.join(path,newname+newfiletype);#新的文件路径

        os.rename(Olddir,Newdir);#重命名
rename();
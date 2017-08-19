#coding:utf-8
import os
import codecs,sys
import string
import re
import math
from GetFileFromDir import GetFileFromThisRootDir
import shutil

def rename():
    parentpath = r'E:\GoogleEarth\赵泽宽\checkded'
    pathlist = os.listdir(parentpath)

    for dir in pathlist:

        print('dir: ', dir)
        dir2 = os.path.join(parentpath, dir)
        print('dir2: ', dir2)


        #while True:
         #   pass
        path = os.path.join(dir2, 'labelTxt')
        outpath = os.path.join(dir2, 'renamelabelTxt')
        if not os.path.isdir(outpath):
            os.mkdir(outpath)
        filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
        for index, files in enumerate(filelist):#遍历所有文件
            Olddir=os.path.join(path,files);#原来的文件路径
            if os.path.isdir(Olddir):#如果是文件夹则跳过
                continue;
            print('Olddir:', Olddir)
            dirsplits = Olddir.split('\\')

            print(dirsplits[-3])
            time = dirsplits[-3].split('-')[0]
            print(time)
            name = os.path.basename(Olddir)
            newname = time + '-' + name
            print('newname: ', newname)
            outname = os.path.join(outpath, newname)
            print('outname:', outname)
            shutil.copyfile(Olddir, outname)
if __name__ == '__main__':
    rename()
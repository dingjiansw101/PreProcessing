#coding:utf-8
import os
import codecs,sys
import string
import re
import math
import numpy as np
import argparse

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
if __name__ == '__main__':
    filelist = GetFileFromThisRootDir(r'E:\20170719', '.tar.gz')
    outpath = r'E:\code\enviscript\names.txt'
    out = open(outpath, 'w')
    print(len(filelist))
    for name in filelist:
        basename = os.path.basename(name)
        print('basename: ', basename)
        id = os.path.splitext(basename)[0]
        id2 = os.path.splitext(id)[0]
        print('id: ', id2)
        out.write(id2 + '\n')
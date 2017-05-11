#coding:utf-8
import os
import numpy as np
import codecs,sys
import txtsplit

class object:
    bbox = np.zeros(8) - 1;
    label = -1;
    hardflag = -2;
test = []
ob1 = object()
ob1.bbox = object.bbox + 3;
ob2 = object()
test.append(ob1)
test.append(ob2)
print(test[0].bbox)
print(test[1].bbox)
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

list = GetFileFromThisRootDir('G:\oldtonew\oldtxt', 'txt');
basedir = 'G:\oldtonew\\newtxt\\';
print(basedir)
for txt in list:
    print(txt)
    txtsplit.txtsplit(txt, basedir)
print(object)
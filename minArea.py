#coding:utf-8
import os
import codecs,sys
import numpy as np
import cv2


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

list = GetFileFromThisRootDir('G:\Data\GoogleMap\标注\dj\Tool\labelTxt', 'txt');
basedir = 'G:\Data\GoogleMap\标注\dj\Tool\labelchange\\';
print(basedir)
print('2**2 = ', 2**2)

for txt in list:
    print('txt', txt)
    f = open(txt, 'r', encoding='utf_16')
    strlist = txt.split('\\');
    filename = strlist[len(strlist) - 1];
    filename = filename[0:(len(filename) - 4)];
    print('yes', filename);
    dir = basedir + filename + '.txt';
    out = codecs.open(dir, 'w', 'utf_16');

    cnt = 0;
    allcnt = 0;
    print(txt)
    #str = '';

    while True:

        allcnt = allcnt + 1;
        print("allcnt", allcnt);
        cnt = cnt + 1;
        line = f.readline();
        if line:
            print(line)
            line = line.strip()
            linelist = line.split(' ');
            print(linelist);
            bbox = linelist[0:8];
            for index, item in enumerate(bbox):
                bbox[index] = float(item);
            print('bbox', bbox);
            leftover = linelist[8:len(linelist)];
            for index, item in enumerate(leftover):
                leftover[index] = int(item);
            print('leftover', leftover);

            cnt = np.array([(bbox[0], bbox[1]), (bbox[2], bbox[3]), (bbox[4], bbox[5]), (bbox[6], bbox[7])], dtype = np.int32);
            print('cnt', cnt);
            rect = cv2.minAreaRect(cnt);
            box = cv2.boxPoints(rect);
            box = np.int0(box)
            print('box', box)
            print('rect', rect);

            outline = ''
            for index, item in enumerate(box):
                print('item', item)
                #box[index] = int(item)
                outline = outline + str(int(item[0])) + ' ' + str(int(item[1])) + ' '
            outline = outline + str(leftover[0])
            if len(leftover) == 2:
                outline = outline + ' ' + str(leftover[1])
            print('outline', outline)
            out.write(outline + '\n');
        else:
            break;
    f.close()
print(object)
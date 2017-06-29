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

list = GetFileFromThisRootDir(r'E:\Data\JINLIN\Txt\labelTxt', 'txt');
basedir = r'E:\Data\JINLIN\Txt\reclabelTxt\\';
print(basedir)
print('2**2 = ', 2**2)
gfclass = {'0A':'plane', '0B':'plane', '0C':'plane', '0':'plane', '2':'bridge', '5':'ship', '5A':'ship', '5B':'ship',
           '8':'storage', '11':'harbor'}
jlclass = {'0':'plane', '2':'bridge', '9':'ship', '6':'harbor', '5':'storage'}
for txt in list:
    print('txt', txt)
    f = open(txt, 'r', encoding='utf_16')
    strlist = txt.split('\\');
    filename = strlist[len(strlist) - 1];
    print('filename', filename)
    suffix = os.path.splitext(filename)[1]
    print('suffix', suffix)
    print('lensuffix', len(suffix))
    filename = filename[0:(len(filename) - len(suffix))];
    print('yes', filename);
    dir = basedir + filename + '.txt';
    print('dir', dir)
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
            #linelist[8] = gfclass[linelist[8]]
            linelist[8] = jlclass[linelist[8]]
            leftover = linelist[8:len(linelist)];

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
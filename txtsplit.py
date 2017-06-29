import os
import codecs
import numpy as np
import math
import tensorflow as tf

wo shi txt-branch
class object:
    bbox = np.zeros(8) - 1;
    label = -1;
    hardflag = -2;
#for i in range(3):
 #   print(i)
#print('str',type(str(2)), 'num', type(2))
testlist = [[]]
testlist[0].append(1)
testlist.append([])
print(testlist)

def txtsplit(txt, basedir):
    print('txt', txt)
    f = open(txt, 'r', encoding='utf_16')
    strlist = txt.split('\\')
    name = strlist[len(strlist) - 1];
    name = name[0:(len(name) - 4)];
    print('yes', name);
    #dir = basedir + str + '.txt';
    #os.mkdir(basedir)


    filelist = []
    for y in range(4):
        filelist.append([])
        for x in range(4):
            dir = basedir + name + '_' + str(y + 1) + '_' + str(x + 1) + '.txt'
            out = codecs.open(dir, 'w', 'utf_16');
            filelist[y].append(out)
    print('filelist', filelist)

    cnt = 0;
    allcnt = 0;
    print(txt)
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
            tmp = object()
            for index, item in enumerate(tmp.bbox):
                tmp.bbox[index] = int(linelist[index])

            if len(linelist) == 10:
                tmp.hardflag = 1
            else:
                tmp.hardflag = 0;
            if (len(linelist) >= 9):
                tmp.label = int(linelist[8])
            ###determine the box belong to which patch
            stride_x = tmp.bbox[0]/4000 + 1
            stride_y = tmp.bbox[1]/4000 + 1
            if (stride_x > 4):
                stride_x = 4
            if (stride_y > 4):
                stride_y = 4
            stride_x = math.floor(stride_x)
            stride_y = math.floor(stride_y)
            flag = True
            print('stride_x', stride_x, 'stride_y', stride_y)
            for i in range(3):
                tmp_x = tmp.bbox[2 + i*2]/4000 + 1
                tmp_y = tmp.bbox[2 + i*2 + 1]/4000 + 1
                if (tmp_x > 4):
                    tmp_x = 4
                if (tmp_y > 4):
                    tmp_y = 4
                tmp_x = math.floor(tmp_x)
                tmp_y = math.floor(tmp_y)
                print('tmp_x', tmp_x, 'tmp_y', tmp_y)
                if (stride_x != tmp_x) or (stride_y != tmp_y) :
                    flag = False
                    break
            if flag:
                for i in range(4):
                    tmp.bbox[i*2] = int(tmp.bbox[i*2] - 4000*(stride_x-1))
                for i in range(4):
                    tmp.bbox[1 + i*2] = int(tmp.bbox[1 + i*2] - 4000*(stride_y - 1))

                outline = ''
                print('writing')
                for item in tmp.bbox:
                    outline = outline + str(int(item)) + ' '
                if (tmp.label != -1):
                    outline = outline + str(tmp.label) + ' '
                if (tmp.hardflag):
                    outline = outline + str(1)
                filelist[stride_y - 1][stride_x - 1].write(outline + '\n')
                #out.write(line + '\n');
        else:
            break;
    f.close()
#txt = 'G:\oldtonew\oldtxt\JL101A_PMS_20160518022947_000008798_202_0011_001_L1_PAN.txt'
#dir = 'G:\oldtonew\\newtxt\\'
#txtsplit(txt, dir)
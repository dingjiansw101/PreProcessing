import os
import utils as util
import nms as polynms
import numpy as np
import re

def nmsbynamedict(nameboxdict, nmsway, thresh):
    nameboxnmsdict = {x: [] for x in nameboxdict}
    for imgname in nameboxdict:
        #print('imgname:', imgname)
        #keep = py_cpu_nms(np.array(nameboxdict[imgname]), thresh)
        #print('type nameboxdict:', type(nameboxnmsdict))
        #print('type imgname:', type(imgname))
        #print('type nms:', type(nms))
        keep = nmsway(np.array(nameboxdict[imgname]), thresh)
        outdets = []
        for index in keep:
            outdets.append(nameboxdict[imgname][index])
        nameboxnmsdict[imgname] = outdets
    return nameboxnmsdict
def poly2origpoly(poly, x, y):
    origpoly = []
    for i in range(int(len(poly)/2)):
        tmp_x = poly[i * 2] + x
        tmp_y = poly[i * 2 + 1] + y
        origpoly.append(tmp_x)
        origpoly.append(tmp_y)
    return origpoly




def parsepolyresults(filename):
    objects = []
    #print('filename: ', filename)
    with open(filename, 'r') as f:
        lines = f.readlines()
        splitlines = [x.strip().split(',') for x in lines]
        for splitline in splitlines:
            #print('splitline:', splitline)
            object_struct = {}
            object_struct['poly'] = splitline[0:8]
            object_struct['score'] = splitline[8]
            object_struct['name'] = splitline[9]
            objects.append(object_struct)
    return objects

def integratefaster_rcnnresults(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    comp4dict = {}
    for fullname in filelist:
        objects = parsepolyresults(fullname)
        for obj in objects:
            wordname = obj['name']
            poly = obj['poly']
            confidence = obj['score']
            subname = util.mybasename(fullname)[4:]
            if (wordname not in comp4dict):
                dstname = os.path.join(dstpath, 'comp4_det_test_' + wordname + '.txt')
                comp4dict[wordname] = open(dstname, 'w')
            outline = subname + ' ' + str(confidence) + ' ' + ' '.join(poly)
            comp4dict[wordname].write(outline + '\n')

def test():
    integratefaster_rcnnresults(r'/home/dj/faster-rcnn/output/rcnn/bod/bod/test/test_results',
                                r'/home/dj/faster-rcnn/output/rcnn/bod/bod/test/comp4_test_results')
if __name__ == '__main__':
    test()
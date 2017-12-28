import os
import codecs
import numpy as np
import math
from GetFileFromDir import GetFileFromThisRootDir
import argparse
import cv2
import shapely.geometry as shgeo
import utils as util
import re
import nms as polynms

nms_thresh = 0.3
def py_cpu_nms(dets, thresh):
    """Pure Python NMS baseline."""
    #print('dets:', dets)
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = dets[:, 4]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    ## index for dets
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= thresh)[0]
        order = order[inds + 1]

    return keep
def cpu_nums_poly(boxes, overlap):
    nms_flag = polynms.nms(boxes, overlap)
    keep = []
    for index, item in enumerate(nms_flag):
        if item:
            keep.append(index)
    return keep
def nmsbynamedict(nameboxdict, nms, thresh):
    nameboxnmsdict = {x: [] for x in nameboxdict}
    for imgname in nameboxdict:
        #print('imgname:', imgname)
        #keep = py_cpu_nms(np.array(nameboxdict[imgname]), thresh)
        #print('type nameboxdict:', type(nameboxnmsdict))
        #print('type imgname:', type(imgname))
        #print('type nms:', type(nms))
        keep = nms(np.array(nameboxdict[imgname]), thresh)
        #print('keep:', keep)
        outdets = []
        #print('nameboxdict[imgname]: ', nameboxnmsdict[imgname])
        for index in keep:
            print('index:', index)
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
def py_cpu_nms_poly(dets, thresh):
    scores = dets[:, 8]
    polys = []
    areas = []
    for i in range(len(dets)):
        tm_polygon = shgeo.Polygon([(dets[i][0], dets[i][1]),
                                    (dets[i][2], dets[i][3]),
                                    (dets[i][4], dets[i][5]),
                                    (dets[i][6], dets[i][7])
                                    ])
        polys.append(tm_polygon)
        areas.append(tm_polygon.area)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        ovr = []
        i = order[0]
        keep.append(i)
        for j in range(order.size - 1):
            inter_poly = polys[order[0]].intersection(polys[order[order[j + 1]]])
            inter_area = inter_poly.area
            ovr.append(inter_area / (areas[i] + areas[order[j + 1]] - inter_area))
        ovr = np.array(ovr)
        inds = np.where(ovr <= thresh)[0]
        order = order[inds + 1]
    return keep

def mergebase(srcpath, dstpath, nms):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for fullname in filelist:
        name = util.mybasename(fullname)
        #print('name:', name)
        dstname = os.path.join(dstpath, name + '.txt')
        with open(fullname, 'r') as f_in:
            nameboxdict = {}
            lines = f_in.readlines()
            splitlines = [x.strip().split(' ') for x in lines]
            for splitline in splitlines:
                subname = splitline[0]
                splitname = subname.split('__')
                oriname = splitname[0]
                pattern1 = re.compile(r'__\d+___\d+')
                x_y = re.findall(pattern1, subname)
                x_y_2 = re.findall(r'\d+', x_y[0])
                x, y = int(x_y_2[0]), int(x_y_2[1])
                confidence = splitline[1]
                poly = list(map(float, splitline[2:]))
                origpoly = poly2origpoly(poly, x, y)
                det = origpoly
                det.append(confidence)
                det = list(map(float, det))
                if (oriname not in nameboxdict):
                    nameboxdict[oriname] = []
                nameboxdict[oriname].append(det)
            nameboxnmsdict = nmsbynamedict(nameboxdict, nms, nms_thresh)
            with open(dstname, 'w') as f_out:
                for imgname in nameboxnmsdict:
                    for det in nameboxnmsdict[imgname]:
                        #print('det:', det)
                        confidence = det[-1]
                        bbox = det[0:-1]
                        outline = imgname + ' ' + str(confidence) + ' ' + ' '.join(map(str, bbox))
                        #print('outline:', outline)
                        f_out.write(outline + '\n')
def mergebyrec():
    srcpath = r'E:\bod-dataset\results\bod_faster_v2_1028498'
    dstpath = r'E:\bod-dataset\results\bod_faster_v2_1028498-nms'
    mergebase(srcpath,
              dstpath,
              py_cpu_nms)
def mergebypoly():
    srcpath = r'/home/dj/faster-rcnn/output/rcnn/bod/bod/test/comp4_test_results'
    dstpath = r'/home/dj/faster-rcnn/output/rcnn/bod/bod/test/comp4_test_nms_0.1'
    mergebase(srcpath,
              dstpath,
              cpu_nums_poly)

if __name__ == '__main__':
    #mergebypoly()
    mergebyrec()
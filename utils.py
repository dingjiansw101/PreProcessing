#-----------------------------------------
# some frequently used functions in data, and file process
# way of naming:
# for example, a full path name E:\code\Test\labelTxt2\1.txt, then
# basename indicates 1.txt, name indicates 1, suffix indicates .txt, path indicates E:\code\Test\labelTxt2, dir indicates E:\code\Test\labelTxt2\1.txt
# written by Jian Ding
#-----------------------------------------
## warp to calculate the set union, difference and intersection of files in two paths, not include the suffix, need to add by yourself
import os
import xml.etree.ElementTree as ET
import codecs
import cv2
import sys
import numpy as np
import random
import shutil
import shapely.geometry as shgeo
datamap = {'0A': 'passenger plane', '0B': 'fighter aeroplane', '0C': 'radar warning aircraft',
           '1': 'baseball diamond', '2': 'bridge', '3': 'ground track', '4A': 'car', '4B': 'truck',
           '4C': 'bus', '5A': 'ship', '5': 'ship', '5B': 'warship', '6': 'tennis court', '7': 'Basketball court',
           '7B': 'half basketball', '8': 'storage tank', '9': 'soccer ball field', '10': 'Turntable',
           '11': 'harbor', '12': 'electric pole', '13': 'parking lot', '14': 'swimming pool', '15': 'lake',
           '16': 'helicopter', '17': 'airport', '18A': 'viaduct', '18B': '18B', '18C': '18C', '18D': '18D',
           '18E': '18E', '18F': '18F', '18G': '18G', '18H': '18H', '18I': '18I', '18J': '18J', '18K': '18K',
           '18L': '18L', '18M': '18M', '18N': '18N', '4A_area': '4A_area', '4B_area': '4B_area',
           '5A_area': '5A_area', '8_area': '8_area', '13_area': '13_area', 'bridge': 'bridge', 'plane': 'plane',
           'ship': 'ship', 'storage': 'storage', 'harbor': 'harbor'}

classname = ['0A', '0B', '0C', '1', '2', '3', '4A', '4B', '4C', '5A', '5B', '6', '7', '8', '9', '10'
    , '11', '12', '13', '14', '15', '16', '17', '18A', '18B', '18C', '18D', '18E'
    , '18F', '18G', '18H', '18I', '18J', '18K', '18L', '18M', '18N', '5', 'plane', 'ship', 'storage', 'bridge',
             'harbor']
clsdict = {'0A': 0, '0B': 0, '0C': 0, '1': 0, '2': 0, '3': 0, '4A': 0, '4B': 0, '4C': 0, '5A': 0, '5B': 0, '6': 0,
           '7': 0, '8': 0, '9': 0, '10': 0
    , '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18A': 0, '18B': 0, '18C': 0, '18D': 0, '18E': 0
    , '18F': 0, '18G': 0, '18H': 0, '18I': 0, '18J': 0, '18K': 0, '18L': 0, '18M': 0, '18N': 0, '5': 0
    , 'plane': 0, 'ship': 0, 'storage': 0, 'bridge': 0, 'harbor': 0}

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

def filesetcalc(path1, path2, calc = ''):
    if calc == '':
        print('please assigh a calc')
        return
    file1_list = GetFileFromThisRootDir(path1)
    file_set1 = {os.path.splitext(os.path.basename(x))[0] for x in GetFileFromThisRootDir(path1)}
    file_set2 = {os.path.splitext(os.path.basename(x))[0] for x in GetFileFromThisRootDir(path2)}
    inter_set = file_set1.intersection(file_set2)
    diff_set = file_set1.difference(file_set2)
    union_set = file_set1.union(file_set2)
    #suffix1 = os.path.splitext(os.path.basename(file1_list[0]))[1]
    if calc == 'u':
        print('union_set:', union_set)
        return union_set
    elif calc == 'd':
        print('diff_dict:', diff_set)
        return diff_set
    elif calc == 'i':
        print('inter_dict:', inter_set)
        return inter_set

def dots2ToRecC(rec):
    xmin, xmax, ymin, ymax = dots2ToRec4(rec)
    x = (xmin + xmax)/2
    y = (ymin + ymax)/2
    w = xmax - xmin
    h = ymax - ymin
    return x, y, w, h

def dots2ToRec4(rec):
    xmin, xmax, ymin, ymax = rec[0], rec[0], rec[1], rec[1]
    for i in range(3):
        xmin = min(xmin, rec[i * 2 + 1])
        xmax = max(xmax, rec[i * 2 + 1])
        ymin = min(ymin, rec[i * 2 + 2])
        ymax = max(ymax, rec[i * 2 + 2])
    return xmin, ymin, xmax, ymax

def dots4ToRec4(poly):
    xmin, xmax, ymin, ymax = min(poly[0][0], min(poly[1][0], min(poly[2][0], poly[3][0]))), \
                            max(poly[0][0], max(poly[1][0], max(poly[2][0], poly[3][0]))), \
                             min(poly[0][1], min(poly[1][1], min(poly[2][1], poly[3][1]))), \
                             max(poly[0][1], max(poly[1][1], max(poly[2][1], poly[3][1])))
    return xmin, ymin, xmax, ymax
def dots4ToRec8(poly):
    xmin, ymin, xmax, ymax = dots4ToRec4(poly)
    return xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax
def parse_rec(filename):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        obj_struct['pose'] = obj.find('pose').text
        obj_struct['truncated'] = int(obj.find('truncated').text)
        obj_struct['difficult'] = int(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)
    return objects

def bod4dotsTo2dots(basepath):
    dots2path = os.path.join(basepath, r'2dotslabelTxt')
    dots4path = os.path.join(basepath, r'labelTxt')
    txtlist = GetFileFromThisRootDir(dots4path, '.txt')
    for txtfile in txtlist:
        objects = parse_bod_poly(txtfile)
        basename = os.path.splitext(os.path.basename(txtfile))[0]
        f_out = codecs.open(os.path.join(dots2path, basename + '.txt'), 'w', 'utf_16')
        for obj in objects:
            bbox = dots4ToRec8(obj['poly'])
            name = obj['name']
            difficult = obj['difficult']
            bbox = list(map(str, bbox))
            outline = ' '.join(bbox)
            outline = outline + ' ' + name
            if difficult:
                outline = outline + ' ' + str(difficult)
            f_out.write(outline + '\n')
def test_bod4dotsTo2dots():
    bod4dotsTo2dots(r'E:\GoogleEarth\up-9-25-data\secondjpg\trainsplit-2')

def bod2pascal(basepath):
    pascalLabel_path = os.path.join(basepath, r'pascalLabel')
    txt_path = os.path.join(basepath, r'labelTxt')
    txtlist = GetFileFromThisRootDir(txt_path, '.txt')
    for txtfile in txtlist:
        objects = parse_bod_poly(txtfile)
        basename = os.path.splitext(os.path.basename(txtfile))[0]
        tree_root = ET.Element('annotation')
        folder = ET.SubElement(tree_root, 'secondjpg')
        filename = ET.SubElement(tree_root, basename)
        size = ET.SubElement(tree_root, 'size')
        width = ET.SubElement(size, 'width')
        height = ET.SubElement(size, 'height')
        ## TODO: read imagesize from img or info
        imgname = os.path.join(basepath, 'images', basename + '.jpg')
        #img = cv2.imread(imgname)
        width.text = str(1024)
        height.text = str(1024)
        for obj in objects:
            object = ET.SubElement(tree_root, 'object')
            ET.dump(tree_root)
            name = ET.SubElement(object, 'name')
            name.text = datamap[obj['name']]
            difficult = ET.SubElement(object, 'difficult')
            print('difficult:', obj['difficult'])
            difficult.text = str(obj['difficult'])
            print('type difficult.text:', type(difficult.text ))
            bndbox = ET.SubElement(object, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            xmax = ET.SubElement(bndbox, 'xmax')
            ymin = ET.SubElement(bndbox, 'ymin')
            ymax = ET.SubElement(bndbox, 'ymax')
            poly = obj['poly']
            bbox = dots4ToRec4(poly)
            xmin.text = str(bbox[0])
            ymin.text = str(bbox[1])
            xmax.text = str(bbox[2])
            ymax.text = str(bbox[3])
        #tree_debug = ET.dump(tree_root)
        tree = ET.ElementTree(tree_root)
        tree.write(os.path.join(pascalLabel_path, basename + '.xml'))
def testtxt2pascal():
    basepath = r'E:\GoogleEarth\up-9-25-data\secondjpg\trainsplit-2'
    bod2pascal(basepath)
def parse_labelme_poly(filename):
    """ Parse a labelme xml file """
    tree = ET.parse(filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        obj_struct['deleted'] = obj.find('deleted').text
        obj_struct['verified'] = int(obj.find('verified').text)
        obj_struct['occluded'] = obj.find('occluded').text
        obj_struct['attributes'] = obj.find('attributes').text
        poly = obj.find('polygon').findall('pt')
        obj_struct['polygon'] = []
        for point in poly:
            pt = [point.find('x').text, point.find('y').text]
            obj_struct['polygon'] = obj_struct['polygon'] + pt
        objects.append(obj_struct)
    return objects
def parse_bod_poly(filename):
    objects = []
    print('filename:', filename)
    f = []
    if (sys.version_info >= (3, 5)):
        fd = open(filename, 'r', encoding = 'utf_16')
        f = fd
    elif (sys.version_info >= 2.7):
        fd = codecs.open(filename,'r', 'utf-16')
        f = fd
    while True:
        line = f.readline()
        if line:
            splitlines = line.strip().split(' ')
            object_struct = {}
            if (len(splitlines) >= 9) and (splitlines[8] in classname):
                object_struct['name'] = splitlines[8]
            else:
                continue
            if (len(splitlines) == 9):
                object_struct['difficult'] = 0
            elif (len(splitlines) >= 10):
                object_struct['difficult'] = 1
            object_struct['poly'] = [(int(float(splitlines[0])), int(float(splitlines[1]))),
                                      (int(float(splitlines[2])), int(float(splitlines[3]))),
                                      (int(float(splitlines[4])), int(float(splitlines[5]))),
                                      (int(float(splitlines[6])), int(float(splitlines[7])))
                                     ]
            gtpoly = shgeo.Polygon(object_struct['poly'])
            object_struct['area'] = gtpoly.area
            objects.append(object_struct)
        else:
            break
    return objects
def getorderLabel(filename):
    f = open(filename, 'r', encoding='utf_16')
    lines = f.readlines()
    splitlines = [x.strip().split(' ') for x in lines]
    labellist = [x[8] for x in splitlines]
    orderlabel = {}
    for cls in clsdict:
        orderlabel[cls] = labellist.count(cls) / len(labellist)
    return orderlabel

def orderdict_byvalue():
    pass
def ImgFormT(srcpath, dstpath, dstform):
    namelist = GetFileFromThisRootDir(srcpath, '.tif')
    for imgname in namelist:
        src = cv2.imread(imgname)
        basename = os.path.splitext(os.path.basename(imgname))[0]
        cv2.imwrite(os.path.join(dstpath, basename + dstform), src)
def testImgTrans():
    basepath = r'E:\GoogleEarth\up-9-25-data'
    dstpath = os.path.join(basepath, 'Secondjpg')
    srcpath = os.path.join(basepath, 'secondQuality')
    ImgFormT(srcpath, dstpath, '.jpg')
def testGenerateClassLabel():
    basepath = r'E:\GAOFEN2\gaofen2Labelme'
    classlabel_path = os.path.join(basepath, 'classlabel')
    labelTxt_path = os.path.join(basepath, 'labelTxt')
    labellist = GetFileFromThisRootDir(labelTxt_path, 'txt')
    for name in labellist:
        basename = os.path.basename(os.path.splitext(name)[0])
        orderlabel = getorderLabel(name)
        print('orderlabel:', orderlabel)
        outline = ''
        with open(os.path.join(classlabel_path, basename + '.txt'), 'w') as f:
            for cls in classname:
                outline = outline + str(cls) + ':' + str(orderlabel[cls]) + ', '
        f.write(outline + '\n')
def labelme2txt(basepath):
    annotations_path = os.path.join(basepath, 'annotations')
    labelTxt_path = os.path.join(basepath, 'labelTxt')
    xmllist = GetFileFromThisRootDir(annotations_path, 'xml')
    for xml in xmllist:
        objects = parse_poly(xml)
        name = os.path.splitext(xml)[0]
        basename = os.path.basename(name)
        print('basename:', basename)
        extent = os.path.splitext(xml)[1]
        with codecs.open(os.path.join(labelTxt_path, basename + '.txt'), 'w', 'utf_16') as f_out:
            for obj in objects:
                if not int(obj['deleted']) :
                    outline = ' '.join(obj['polygon']) + ' ' + obj['name']
                    f_out.write(outline + '\n')
def testparse():
    objects = parse_labelme_poly(r'E:\GAOFEN2\gaofen2Labelme\annotations\singapore-2016-4-27-1.xml')
    print(objects)
def TrainTestSplit():
    basepath = r'E:\GoogleEarth\up-9-25-data\secondjpg'
    filelist = GetFileFromThisRootDir(os.path.join(basepath, 'images'))
    name = [os.path.basename(os.path.splitext(x)[0]) for x in filelist]
    train_len = int(len(name) * 0.6)
    test_len = len(name) - train_len
    print('train_len:', train_len)
    print('test_len:', test_len)
    random.shuffle(name)
    print('shuffle name:', name)
    train_set= set(name[0:train_len])
    test_set = set(name[train_len:])
    print('intersection:', train_set.intersection(test_set))
    for imgname in train_set:
        if (imgname == 'Thumbs'):
            continue
        srcname = os.path.join(basepath, 'images', imgname + '.tif')
        dstname = os.path.join(basepath, 'train', 'images', imgname + '.tif')
        shutil.move(srcname, dstname)
        srctxt = os.path.join(basepath, 'labelTxt', imgname + '.txt')
        dsttxt = os.path.join(basepath, 'train', 'labelTxt', imgname + '.txt')
        print(srctxt)
        print(dsttxt)
        shutil.move(srctxt, dsttxt)
    for imgname in test_set:
        if (imgname == 'Thumbs'):
            continue
        srcname = os.path.join(basepath, 'images', imgname + '.tif')
        dstname = os.path.join(basepath, 'test', 'images', imgname + '.tif')
        shutil.move(srcname, dstname)
        srctxt = os.path.join(basepath, 'labelTxt', imgname + '.txt')
        dsttxt = os.path.join(basepath, 'test', 'labelTxt', imgname + '.txt')
        shutil.move(srctxt, dsttxt)
def py_cpu_nms_poly(dets, thresh):
    scores = dets[:, 8]
    polys = []
    areas = []
    for i in len(dets):
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
        for j in len(order.size - 1):
            inter_poly = polys[order[0]].intersection(polys[order[order[j + 1]]])
            inter_area = inter_poly.area
            ovr.append(inter_area / (areas[i] + areas[order[j + 1]] - inter_area))
        ovr = np.array(ovr)
        inds = np.where(ovr <= thresh)[0]
        order = order([inds + 1])
    return keep
def py_cpu_nms(dets, thresh):
    """Pure Python NMS baseline."""
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = dets[:, 4]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
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
def test_py_cpu_nms():
    dets = np.array([ [0, 0, 4, 4, 0.7],
                        [2, 2, 7, 6, 0.8],
                        [3, 2, 8, 5, 0.6],
                        [0, 0, 7, 7, 0.75]
                    ])
    keep = py_cpu_nms(dets, 0.5)
    print(keep)
def nms_poly(boxes, threshold, type):
    pass
if __name__ == '__main__':
    testtxt2pascal()
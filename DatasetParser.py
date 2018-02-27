import utils as util
import os
import codecs
import re
import xml.etree.ElementTree as ET
import math
import numpy as np
import json

datamap_15 = {'0A': 'plane', '0B':'plane', '0C': 'plane',  '1': 'baseball-diamond', '2': 'bridge', '3': 'ground-track-field', '4A': 'small-vehicle', '4B': 'large-vehicle',
           '4C': 'large-vehicle', '5A': 'ship', '5B':'ship', '6': 'tennis-court', '7': 'basketball-court',
           '8': 'storage-tank', '9': 'soccer-ball-field', '10': 'turntable',
           '11': 'harbor', '14': 'swimming-pool',
           '16': 'helicopter'}
datamap_inverse = {datamap_15[x]:x for x in datamap_15}
class parse_3k_vehicle(object):
    def __init__(self,
                 basepath):
        self.basepath = basepath
        self.classname = ['bus', 'dashed_line', 'pkw', 'truck', 'cam', 'truck_trail', 'van_trail']
        self.datamap = {'10': 'pkw', '11': 'pkw_trail', '22': 'Truck', '23': 'truck_trail',
                        '17': 'van_trail', '20': 'cam', '30': 'bus', '110': 'dashed_line', '16':'N/A'}
        self.prefix_len = 35
    def rotate_point(self, alpha, x):
        return (math.cos(alpha) * x[0] - math.sin(alpha) * x[1], math.sin(alpha) * x[0] + math.cos(alpha) * x[1])

    def rotate_rec(self, alpha, rec):
        x, y, w, h = rec[0], rec[1], rec[2], rec[3]
        p1 = [w, h]
        p2 = [w, -h]
        p3 = [-w, -h]
        p4 = [-w, h]
        outp1 = self.rotate_point(alpha, p1)
        outp2 = self.rotate_point(alpha, p2)
        outp3 = self.rotate_point(alpha, p3)
        outp4 = self.rotate_point(alpha, p4)
        return [
            (outp2[0] + x), (outp2[1] + y),
            (outp1[0] + x), (outp1[1] + y),
            (outp4[0] + x), (outp4[1] + y),
            (outp3[0] + x), (outp3[1] + y),
                ]

    ## TODO: trans it into bod-format

    def parse_3k_VehicleDetection(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        uselines = lines[3:]
        print('uselines: ', uselines)
        splitlines = [x.strip().split(' ') for x in uselines]
        objects = []
        print ('filename:', filename)
        for splitline in splitlines:
            object_struct = {}
            if (len(splitline) < 7):
                continue
            if (splitline[1] not in self.datamap):
                print('category name:', splitline[1])
                continue
            name = self.datamap[splitline[1]]
            object_struct['name'] = name
            object_struct['rotrec'] = splitline[2:]
            x, y, w, h, angle = splitline[2:]
            xmin, ymin, xmax, ymax = int(x) - int(w), int(y) - int(h), int(x) + int(w), int(y) + int(h)
            poly = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
            alpha = float(angle)/180 * math.pi

            #rotate_poly = list(map(lambda x:self.rotate_point(alpha, x), poly))
            rec = list(map(int, (x, y, w, h)))
            rotate_poly = self.rotate_rec(-alpha, rec)
            #rotate_poly = poly
            # object_struct['rotpoly'] = [rotate_poly[0][0],
            #                             rotate_poly[0][1],
            #                             rotate_poly[1][0],
            #                             rotate_poly[1][1],
            #                             rotate_poly[2][0],
            #                             rotate_poly[2][1],
            #                             rotate_poly[3][0],
            #                             rotate_poly[3][1] ]
            object_struct['rotpoly'] = rotate_poly
            objects.append(object_struct)
        return objects

    def trans_3k_Vehicle2bod(self):
        filelist = util.GetFileFromThisRootDir(os.path.join(self.basepath, 'Test'), '.samp')
        outfiledict = {}
        for fullname in filelist:
            objects = self.parse_3k_VehicleDetection(fullname)
            print('fullname:', fullname)
            print('objects:', len(objects))
            imgname = util.mybasename(fullname)[0:35]
            outdir = os.path.join(self.basepath, 'Test_bod', imgname + '.txt')
            print('outdir:', outdir)
            if outdir not in outfiledict:
                outfiledict[outdir] = codecs.open(outdir, 'w', 'utf_16')
            for obj in objects:
                outline = ' '.join(map(str, obj['rotpoly'])) + ' ' + obj['name']
                outfiledict[outdir].write(outline + '\n')

    def count_3k_Vehicle(self):
        testpath = os.path.join(self.basepath, 'Test')
        trainpath = os.path.join(self.basepath, 'Train')
        testnames = util.GetFileFromThisRootDir(testpath, '.samp')
        trainnames = util.GetFileFromThisRootDir(trainpath, '.samp')
        #vehicle_set = {x for x in (testnames + trainnames)}
        vehicle_set = {x for x in trainnames}
        print('file nums:', len(vehicle_set))
        distribution = {}
        for fullname in vehicle_set:
            objects = self.parse_3k_VehicleDetection(fullname)
            for obj in objects:
                if obj['name'] not in distribution:
                    distribution[obj['name']] = 1
                distribution[obj['name']] = distribution[obj['name']] + 1
        print('distribution:', distribution)
def parse_darklabel(filename):
    objects = []
    f = open(filename, 'r')
    lines = f.readlines()
    splitlines = [x.strip().split(' ') for x in lines]
    for splitline in splitlines:
        object_struct = {}
        object_struct['name'] = splitline[0]
        RecC = splitline[1:]
def parsecomp4(srcpath, dstpath):
    thresh = 0.01
    #basepath = r'E:\bod-dataset\results'
    #comppath = os.path.join(basepath, r'bod-rfcn_303888-nms')
    #resultpath = os.path.join(basepath, 'bod_rfcn_303888-txt')
    filedict = {}
    complist = util.GetFileFromThisRootDir(srcpath, '.txt')

    for compfile in complist:
        idname = util.mybasename(compfile).split('_')[-1]
        idname = datamap_inverse[idname]
        f = open(compfile, 'r')
        lines = f.readlines()
        for line in lines:
            if len(line) == 0:
                continue
            splitline = line.strip().split(' ')
            filename = splitline[0]
            confidence = splitline[1]
            bbox = splitline[2:]
            if float(confidence) > thresh:
                if filename not in filedict:
                    filedict[filename] = codecs.open(os.path.join(dstpath, filename + '.txt'), 'w', 'utf_16')
                poly = util.dots2ToRec8(bbox)
                #filedict[filename].write(' '.join(poly) + ' ' + idname + '_' + str(round(float(confidence), 2)) + '\n')
                filedict[filename].write(' '.join(poly) + ' ' + idname  + '\n')
def parsecomp4_poly(srcpath, dstpath):
    thresh = 0.1
    filedict = {}
    complist = util.GetFileFromThisRootDir(srcpath, '.txt')

    for compfile in complist:
        idname = util.mybasename(compfile).split('_')[-1]
        idname = datamap_inverse[idname]
        f = open(compfile, 'r')
        lines = f.readlines()
        for line in lines:
            if len(line) == 0:
                continue
            print('line:', line)
            splitline = line.strip().split(' ')
            filename = splitline[0]
            confidence = splitline[1]
            bbox = splitline[2:]
            if float(confidence) > thresh:
                if filename not in filedict:
                    filedict[filename] = codecs.open(os.path.join(dstpath, filename + '.txt'), 'w', 'utf_16')
                #poly = util.dots2ToRec8(bbox)
                poly = bbox
#               filedict[filename].write(' '.join(poly) + ' ' + idname + '_' + str(round(float(confidence), 2)) + '\n')
            print('idname:', idname)

            #filedict[filename].write(' '.join(poly) + ' ' + idname + '_' + str(round(float(confidence), 2)) + '\n')

            filedict[filename].write(' '.join(poly) + ' ' + idname + '\n')

class parse_hrsc2016(object):
    def __init__(self, basepath):
        self.classname = []
        self.basepath = basepath
    def parse_hrsc_single(self, filename):
        """ Parse a labelme xml file """
        tree = ET.parse(filename)
        objects = []
        for obj in tree.find('HRSC_Objects').findall('HRSC_Object'):
            obj_struct = {}
            obj_struct['class_id'] = obj.find('Class_ID').text
            obj_struct['box_xmin'] = obj.find('box_xmin').text
            obj_struct['box_ymin'] = obj.find('box_ymin').text
            obj_struct['box_xmax'] = obj.find('box_xmax').text
            obj_struct['box_ymax'] = obj.find('box_ymax').text
            objects.append(obj_struct)
        return objects
    def count(self):
        test_gtpath = os.path.join(self.basepath, 'Test', 'Annotations')
        train_gtpath = os.path.join(self.basepath, 'Train', 'Annotations')
        testfiles = util.GetFileFromThisRootDir(test_gtpath)
        trainfiles = util.GetFileFromThisRootDir(train_gtpath)
        #testset = {util.mybasename(x.strip()) for x in testfiles}
        #trainset = {util.mybasename(x.strip()) for x in trainfiles}
        test_sum = 0
        for fullname in testfiles:
            objects = self.parse_hrsc_single(fullname)
            test_sum = test_sum + len(objects)
        train_sum = 0
        for fullname in trainfiles:
            objects = self.parse_hrsc_single(fullname)
            train_sum = train_sum + len(objects)
        print('train_sum: ', train_sum)
        print('test_sum: ', test_sum)

class wider_face_parser():
    def __init__(self,
                 basepath):
        self.basepath = basepath

    def parse_gt(self, filename):
        gt_dict = {}
        with open(filename, 'r') as f:
            lines = f.readlines()
            pos = 0
            while (pos < len(lines)):
                objects = []
                if '.jpg' in lines[pos] :
                    num = int(lines[pos + 1].strip())
                    splitlines = [x.strip().split(' ') for x in lines[(pos + 2): (pos + 2 + num)]]

                    pos = pos + 2 + num
    def countSingle(self, filename):
        gt_dict = {}
        with open(filename, 'r') as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                if '.jpg' in line:
                    num = int(lines[index + 1].strip())
                    gt_dict[line.strip()] = num
        return gt_dict
    def count(self):
        trainpath = os.path.join(self.basepath, 'wider_face_train_bbx_gt.txt')
        traindict = self.countSingle(trainpath)
        trainnum = [traindict[x] for x in traindict]
        testpath = os.path.join(self.basepath, 'wider_face_val_bbx_gt.txt')
        testdict = self.countSingle(testpath)
        testnum = [testdict[x] for x in testdict]

def parsenwpubod():
    datamap = {'1': 'plane', '2': 'ship', '3': 'storage-tank', '4': 'baseball-diamond', '5': 'tennis-court',
               '6': 'basketball-court', '7': 'ground-track-field', '8': 'harbor', '9': 'bridge', '10': 'small-vehicle'}
    numperclass = {'plane':0, 'ship': 0, 'storage-tank': 0, 'baseball-diamond': 0, 'tennis-court': 0,
                   'basketball-court': 0, 'ground-track-field': 0, 'harbor': 0, 'bridge': 0, 'small-vehicle': 0}
    filelist = util.GetFileFromThisRootDir(r'E:\downloaddataset\NWPU\NWPU\labelTxt')
    for fullname in filelist:
        objects = util.parse_bod_poly(fullname)
        for obj in objects:
            wordname = datamap[obj['name']]
            numperclass[wordname] = numperclass[wordname] + 1
    print(numperclass)

def parse_voc(filename):
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
        w, h = int(bbox.find('xmax').text) - int(bbox.find('xmin').text), int(bbox.find('ymax').text) - int(bbox.find('ymin').text)
        obj_struct['size'] = max(w, h)
        objects.append(obj_struct)

    return objects

def parsecoco():
    path = r'E:\downloaddataset\coco'
    trainfile = os.path.join(path, 'instances_train2017.json')
    testfile = os.path.join(path, 'instances_val2017.json')

## vehicle equals others
vedaidict = {'1': 'car', '2': 'truck', '23': 'ship', '4': 'tractor', '5': 'camping car', '9': 'van',
             '10': 'vehicle', '11': 'pick-up', '31': 'plane'}

def parsevedai(fullname):
    objects = []
    with open(fullname, 'r') as f:
        lines = f.readlines()
        splitlines = [x.strip().split(' ') for x in lines]
        for splitline in splitlines:
            object_struct = {}
            classid = splitline[3]
            wordname = vedaidict[classid]
            if (splitline[4] == 1) and (splitline[5] == 0):
                difficult = 0
            else:
                difficult = 1
            object_struct['name'] = wordname
            object_struct['difficult'] = difficult
            object_struct['poly'] = splitline[6:]
            objects.append(object_struct)
    return objects
def vedai2bod(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for fullname in filelist:
            basename = util.mybasename(fullname)
            outname = os.path.join(dstpath, basename + '_co.txt')
            objects = parsevedai(fullname)
            with open(outname, 'w') as f_out:
                    for obj in objects:
                        poly = obj['poly']
                        wordname = obj['name']
                        difficult = obj['difficult']
                        outline = ' '.join(map(str, poly)) + ' ' + wordname + ' ' + str(difficult)
                        f_out.write(outname + '\n')


def testparsevedai():
    parsevedai(r'E:\downloaddataset\VEDAI\Vehicules1024\Vehicules1024\Vehicules1024\bodformat\vehiculesannotation',
               )
compress_data_map = {'bus': 'large-vehicle', 'pkw': 'small-vehicle', 'truck_trail': 'large-vehicle', 'Truck': 'large-vehicle',
                    'pkw_trail': 'small-vehicle', 'cam': 'large-vehicle', 'van_trail': 'large-vehicle', 'N/A': 'small-vehicle'}
def compress3kinto2class(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for fullname in filelist:
        objects = util.parse_bod_poly2(fullname)
        imgname = util.mybasename(fullname)
        dstimgname = os.path.join(dstpath, imgname + '.txt')
        with codecs.open(dstimgname, 'w', 'utf_16') as f_out:
            for obj in objects:
                poly = obj['poly']
                wordname = obj['name']
                if wordname not in compress_data_map:
                    continue
                dstcategory = compress_data_map[wordname]
                outline = ' '.join(map(str, poly)) + ' ' + dstcategory
                f_out.write(outline + '\n')

def bbox2poly(bbox):
    x, y, w, h = bbox
    xmin, ymin = x, y
    xmax = xmin + w
    ymax = ymin + h
    return xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax

def parse_fMoW(filename):
    objects = []
    with open(filename, 'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)

        boxes = load_dict['bounding_boxes']
        for box in boxes:
            object = {}
            object['name'] = box['category']
            rec = box['box']
            object['poly'] = bbox2poly(rec)
            objects.append(object)
    return objects
#    print(load_dict['bounding_boxes'])

def flow2dota(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath, '.json')
    for filename in filelist:
        objects = parse_fMoW(filename)
        basename = util.mybasename(filename)
        outname = os.path.join(dstpath, basename + '.txt')
        with codecs.open(outname, 'w', 'utf-16') as f_out:
            for obj in objects:
                outline = ' '.join(map(str, obj['poly'])) + ' ' + obj['name']
                f_out.write(outline + '\n')

if __name__ == '__main__':
    #face_parser = wider_face_parser(r'E:\downloaddataset\wide_faces\wider_face_split\wider_face_split')
    #parsecomp4()
    # parser = parse_3k_vehicle(r'E:\downloaddataset\3K_VehicleDetection_dataset')
    # parser.trans_3k_Vehicle2bod()
    # compress3kinto2class(r'E:\downloaddataset\3K_VehicleDetection_dataset\Test_bod\labelTxt',
    #                       r'E:\downloaddataset\3K_VehicleDetection_dataset\Test_bod\wordlabel')
    # parsecomp4_poly(r'E:\bod-dataset\results\faster-rcnn-rot-59\nms0.1\comp4_test_nms_0.1',
    #                 r'E:\bod-dataset\results\faster-rcnn-rot-59\nms0.1\wordlabel')
    parsecomp4(r'E:\bod-dataset\results\dota608_ssd608_total_1243788_nms',
               r'E:\bod-dataset\results\dota608_ssd608_total_1243788_nms_labelTxt')
    # flow2dota(r'I:\fMoW\fMoW-rgb_trainval_v1.0.0\fMoW-rgb\train\airport_hangar',
    #           r'I:\fMoW\fMoW-rgb_trainval_v1.0.0\fMoW-rgb\dotaformat\labelTxt')
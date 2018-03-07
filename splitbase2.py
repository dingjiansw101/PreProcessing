import os
import codecs
import numpy as np
import math
from GetFileFromDir import GetFileFromThisRootDir
import argparse
import cv2
import sympy.geometry as geo
import shapely.geometry as shgeo
import utils as util
import copy

outlier1 = 0
outlier2 = 0


def choose_best_pointorder_fit_another(poly1, poly2):
    x1 = poly1[0]
    y1 = poly1[1]
    x2 = poly1[2]
    y2 = poly1[3]
    x3 = poly1[4]
    y3 = poly1[5]
    x4 = poly1[6]
    y4 = poly1[7]
    combinate = [np.array([x1, y1, x2, y2, x3, y3, x4, y4]), np.array([x2, y2, x3, y3, x4, y4, x1, y1]),
                 np.array([x3, y3, x4, y4, x1, y1, x2, y2]), np.array([x4, y4, x1, y1, x2, y2, x3, y3])]
    dst_coordinate = np.array(poly2)
    distances = np.array([np.sum((coord - dst_coordinate)**2) for coord in combinate])
    sorted = distances.argsort()
    return combinate[sorted[0]]

def choose_best_begin_point(pre_result):
    final_result = []
    for coordinate in pre_result:
        x1 = coordinate[0][0]
        y1 = coordinate[0][1]
        x2 = coordinate[1][0]
        y2 = coordinate[1][1]
        x3 = coordinate[2][0]
        y3 = coordinate[2][1]
        x4 = coordinate[3][0]
        y4 = coordinate[3][1]
        xmin = min(x1, x2, x3, x4)
        ymin = min(y1, y2, y3, y4)
        xmax = max(x1, x2, x3, x4)
        ymax = max(y1, y2, y3, y4)
        combinate = [[[x1, y1], [x2, y2], [x3, y3], [x4, y4]], [[x2, y2], [x3, y3], [x4, y4], [x1, y1]], [[x3, y3], [x4, y4], [x1, y1], [x2, y2]], [[x4, y4], [x1, y1], [x2, y2], [x3, y3]]]
        dst_coordinate = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
        force = 100000000.0
        force_flag = 0
        for i in range(4):
            temp_force = cal_line_length(combinate[i][0], dst_coordinate[0]) + cal_line_length(combinate[i][1], dst_coordinate[1]) + cal_line_length(combinate[i][2], dst_coordinate[2]) + cal_line_length(combinate[i][3], dst_coordinate[3])
            if temp_force < force:
                force = temp_force
                force_flag = i
        if force_flag != 0:
            print("choose one direction!")
        final_result.append(combinate[force_flag])
    return final_result

def cal_line_length(point1, point2):
    return math.sqrt( math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))


class splitbase():
    def __init__(self,
                 basepath,
                 outpath,
                 gap=512,
                 subsize=1024,
                 thresh=0.7,
                 choosebestpoint=False
                 ):
        self.basepath = basepath
        self.outpath = outpath
        self.gap = gap
        self.subsize = subsize
        self.slide = self.subsize - self.gap
        self.thresh = thresh
        self.imagepath = os.path.join(self.basepath, 'images')
        self.labelpath = os.path.join(self.basepath, 'wordlabel')
        self.orilabelpath = os.path.join(self.basepath, 'orilabelTxt')
        #self.labelpath = os.path.join(self.basepath, 'labelTxt')
        self.outimagepath = os.path.join(self.outpath, 'images')
        self.outlabelpath = os.path.join(self.outpath, 'wordlabel')
        self.outorilabelpath = os.path.join(self.outpath, 'oriwordlabel')
        #self.outlabelpath = os.path.join(self.outpath, 'labelTxt')
        self.choosebestpoint = choosebestpoint
        with open(os.path.join(self.outpath, 'cutcfg.txt'), 'w') as f_cfg:
            f_cfg.write('gap:' + str(gap) + '\n')
            f_cfg.write('subsize:' + str(subsize))

        self.f_sub = open(os.path.join(self.outpath, 'suborigmap.txt'), 'w')

    ## point: (x, y), rec: (xmin, ymin, xmax, ymax)
    #def PointInpoly(point, poly):
    def __del__(self):
        self.f_sub.close()
    ## grid --> (x, y) position of grids
    def polyorig2sub(self, left, up, poly):
        polyInsub = np.zeros(len(poly))
        for i in range(int(len(poly)/2)):
            polyInsub[i * 2] = int(poly[i * 2] - left)
            polyInsub[i * 2 + 1] = int(poly[i * 2 + 1] - up)
        return polyInsub

    # def polyorig2sub2(self, left, up, poly):
    #     polyInsub = np.zeros(2 * len(poly))
    #     for i in len(poly):
    #         polyInsub[i * 2] = int(poly[i][0] - left)
    #         polyInsub[i * 2 + 1] = int(poly[i][1] - up)
    #     return polyInsub
    ## calc the intersection / poly1
    def calchalf_iou(self, poly1, poly2):
        inter_poly = poly1.intersection(poly2)
        inter_area = inter_poly.area
        poly1_area = poly1.area
        half_iou = inter_area / poly1_area
        return inter_poly, half_iou


    ## this fuction may have problem; the problem solved by using deepcopy
    def saveimagepatches(self, img, subimgname, left, up):
        subimg = copy.deepcopy(img[up: (up + self.subsize), left: (left + self.subsize)])
        outdir = os.path.join(self.outimagepath, subimgname + '.jpg')
        cv2.imwrite(outdir, subimg)

    def saveimagepatcheswithmask(self, img, subimgname, left, up, right, down, mask_poly):
        subimg = copy.deepcopy(img[up: (up + self.subsize), left: (left + self.subsize)])
        for mask in mask_poly:
            bound = mask.bounds
            if (len(bound) < 4):
                continue
            xmin, ymin, xmax, ymax = bound[0], bound[1], bound[2], bound[3]
            for x in range(int(xmin), int(xmax)):
                for y in range(int(ymin), int(ymax)):
                    point = shgeo.Point(x, y)
                    if point.within(mask):
                        #print('withing')
                        #print('left:', left, 'up:', up)
                        subimg[int(y - up - 1)][int(x - left - 1)] = 0
        outdir = os.path.join(self.outimagepath, subimgname + '.jpg')
        cv2.imwrite(outdir, subimg)

    def GetPoly4FromPoly5(self, poly):
        #print('>>>>>>>>>>>>>>>>>>>')
        distances = [cal_line_length((poly[i * 2], poly[i * 2 + 1] ), (poly[(i + 1) * 2], poly[(i + 1) * 2 + 1])) for i in range(int(len(poly)/2 - 1))]
        #print('{{{{{{{{{{{{{{{{{{{{{{')
        distances.append(cal_line_length((poly[0], poly[1]), (poly[8], poly[9])))
        #print('}}}}}}}}}}}}}}}}}}}}}}}}')
        pos = np.array(distances).argsort()[0]
        #print('<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        count = 0
        outpoly = []
        while count < 5:
            #print('count:', count)
            if (count == pos):
                outpoly.append((poly[count * 2] + poly[(count * 2 + 2)%10])/2)
                outpoly.append((poly[(count * 2 + 1)%10] + poly[(count * 2 + 3)%10])/2)
                #print('..................')
                #outpoly.append(poly[count * 2])
                #outpoly.append(poly[count * 2 + 1])
                count = count + 1
            elif (count == (pos + 1)%5):
                count = count + 1
                continue

            else:
                outpoly.append(poly[count * 2])
                outpoly.append(poly[count * 2 + 1])
                count = count + 1
        return outpoly

    ## TODO
    ##def GetPoly4FromPoly5_byborder(self, poly, left, up, right, down):
        #pass
    def savepatches(self, resizeimg, objects, subimgname, left, up, right, down):
        outdir = os.path.join(self.outlabelpath, subimgname + '.txt')
        mask_poly = []
        imgpoly = shgeo.Polygon([(left, up), (right, up), (right, down),
                                 (left, down)])
        with codecs.open(outdir, 'w', 'utf_16') as f_out:
            for obj in objects:
                gtpoly = shgeo.Polygon([(obj['poly'][0], obj['poly'][1]),
                                         (obj['poly'][2], obj['poly'][3]),
                                         (obj['poly'][4], obj['poly'][5]),
                                         (obj['poly'][6], obj['poly'][7])])
                #gtpoly = shgeo.Polygon(obj['poly'])
                if (gtpoly.area <= 0):
                    continue
                inter_poly, half_iou = self.calchalf_iou(gtpoly, imgpoly)

                # print('writing...')
                if (half_iou == 1):
                    polyInsub = self.polyorig2sub(left, up, obj['poly'])
                    outline = ' '.join(list(map(str, polyInsub)))
                    outline = outline + ' ' + obj['name'] + ' ' + str(obj['difficult'])
                    f_out.write(outline + '\n')
                elif (half_iou > 0):
                #elif (half_iou > self.thresh):
                  ##  print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                    inter_poly = shgeo.polygon.orient(inter_poly, sign=1)
                    out_poly = list(inter_poly.exterior.coords)[0: -1]
                    if len(out_poly) < 4:
                        continue

                    out_poly2 = []
                    for i in range(len(out_poly)):
                        out_poly2.append(out_poly[i][0])
                        out_poly2.append(out_poly[i][1])

                    #print('!!!!!!!!!!!!!!!!!!!!!')
                    if (len(out_poly) == 5):
                        #print('==========================')
                        out_poly2 = self.GetPoly4FromPoly5(out_poly2)
                    elif (len(out_poly) > 5):
                        continue
                    if (self.choosebestpoint):
                        out_poly2 = choose_best_pointorder_fit_another(out_poly2, obj['poly'])

                      # polyInsub = self.polyorig2sub(left, up, obj['poly'])
                    polyInsub = self.polyorig2sub(left, up, out_poly2)

                    for index, item in enumerate(polyInsub):
                        if (item <= 1):
                            polyInsub[index] = 1
                        elif (item >= self.subsize):
                            polyInsub[index] = self.subsize
                    outline = ' '.join(list(map(str, polyInsub)))
                    if (half_iou > self.thresh):
                        outline = outline + ' ' + obj['name'] + ' ' + str(obj['difficult'])
                    else:
                        outline = outline + ' ' + obj['name'] + ' ' + '1'
                    f_out.write(outline + '\n')
                #else:
                 #   mask_poly.append(inter_poly)
        #self.saveimagepatches(resizeimg, subimgname, left, up)

    def SplitSingle(self, name, rate, extent):
        img = cv2.imread(os.path.join(self.imagepath, name + extent))
        if np.shape(img) == ():
            return
        fullname = os.path.join(self.labelpath, name + '.txt')
        objects = util.parse_bod_poly2(fullname)
        for obj in objects:
            obj['poly'] = list(map(lambda x:rate*x, obj['poly']))
            #obj['poly'] = list(map(lambda x: ([2 * y for y in x]), obj['poly']))

        if (rate != 1):
            resizeimg = cv2.resize(img, None, fx=rate, fy=rate, interpolation = cv2.INTER_CUBIC)
        else:
            resizeimg = img
        outbasename = name + '__' + str(rate) + '__'
        weight = np.shape(resizeimg)[1]
        height = np.shape(resizeimg)[0]

        left, up = 0, 0
        while (left < weight):
            if (left + self.subsize >= weight):
                left = max(weight - self.subsize, 0)
            up = 0
            while (up < height):
                if (up + self.subsize >= height):
                    up = max(height - self.subsize, 0)
                right = min(left + self.subsize, weight - 1)
                down = min(up + self.subsize, height - 1)
                subimgname = outbasename + str(left) + '___' + str(up)
                self.f_sub.write(name + ' ' + subimgname + ' ' + str(left) + ' ' + str(up) + '\n')
                self.savepatches(resizeimg, objects, subimgname, left, up, right, down)
                if (up + self.subsize >= height):
                    break
                else:
                    up = up + self.slide
            if (left + self.subsize >= weight):
                break
            else:
                left = left + self.slide

    def splitdata_half(self, imgenames):
         for name in imgenames:
             self.SplitSingle(name, 0.5, '.jpg')
    def splitdata(self, imgenames):
         for name in imgenames:
             self.SplitSingle(name, 1, '.jpg')
    def splitdata_2(self, imagenames):
        for name in imagenames:
            self.SplitSingle(name, 2, '.jpg')

    def run(self):
        imagelist = GetFileFromThisRootDir(self.imagepath)
        imagenames = [util.mybasename(x) for x in imagelist if (util.mybasename(x) != 'Thumbs')]
        #self.splitdata_half(imagenames)
        #self.splitdata_2(imagenames)
        self.splitdata(imagenames)
if __name__ == '__main__':
    # split = splitbase(r'E:\bod-dataset',
    #                   r'E:\bod-dataset\cuttestpath')
    split = splitbase(r'/data/Data_dj/data/bod-ori/oriwordlabel',
                       r'/data/Data_dj/data/bod-v3/oriwordlabel')
    split.run()
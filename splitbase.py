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

outlier1 = 0
outlier2 = 0

class splitbase():
    def __init__(self,
                 basepath,
                 outpath,
                 gap=80,
                 subsize=1024,
                 thresh=0.8,
                 ):
        self.basepath = basepath
        self.outpath = outpath
        self.gap = gap
        self.subsize = subsize
        self.thresh = thresh
        self.imagepath = os.path.join(self.basepath, 'images')
        self.labelpath = os.path.join(self.basepath, 'wordlabel')
        self.outimagepath = os.path.join(self.outpath, 'images')
        self.outlabelpath = os.path.join(self.outpath, 'wordlabel')

        with open(os.path.join(self.outpath, 'cutcfg.txt'), 'w') as f_cfg:
            f_cfg.write('gap:' + str(gap) + '\n')
            f_cfg.write('subsize:' + str(subsize))

    ## point: (x, y), rec: (xmin, ymin, xmax, ymax)
    def PointInRec(point, rec):
        return (rec[0] < point[0]) and (point[0] < rec[2]) and (rec[1] < point[1]) and (point[1] < rec[3])
    ## grid --> (x, y) position of grids
    def polyorig2sub(self, grid, poly):
        leftup_x = math.floor(grid[0] * (self.subsize - self.gap))
        leftup_y = math.floor(grid[1] * (self.subsize - self.gap))
        polyInsub = np.zeros(8)
        for i in range(4):
            polyInsub[i * 2] = int(poly[i * 2] - leftup_x)
            polyInsub[i * 2 + 1] = int(poly[i * 2 + 1] - leftup_y)
        return polyInsub
    ## calc the intersection / poly1
    def calchalf_iou(self, poly1, poly2):
        inter_poly = poly1.intersection(poly2)
        inter_area = inter_poly.area
        poly1_area = poly1.area
        half_iou = inter_area / poly1_area
        return half_iou
    def txtsplit(self, imagesize, objects, outbasename, gap, subsize):
        grid_m = int((imagesize[0] - gap)/(subsize - gap))
        grid_n = int((imagesize[1] - gap)/(subsize - gap))
        def GetGrid(poly):
        ## direct calc the position
        ## n correspond to x, m correspond to y
        ## divide by (subsize - gap)
            grids = []
            for i in range(4):
                ggrid_x, ggrid_y = int((poly[i * 2]) / (subsize - gap)), int(
                    (poly[i * 2 + 1]) / (subsize - gap))
                if (ggrid_x, ggrid_y) not in grids:
                    grids.append((ggrid_x, ggrid_y))
                grid_xp, grid_yp = ggrid_x, ggrid_y
                if ((ggrid_x * (subsize - gap) + gap) > poly[i * 2]):
                    grid_xp = max(ggrid_x - 1, 0)
                if ((ggrid_y * (subsize - gap) + gap) > poly[i * 2 + 1]):
                    grid_yp = max(ggrid_y - 1, 0)
                if (grid_xp, grid_yp) not in grids:
                    grids.append((grid_xp, grid_yp))
            return  grids
        ## keys' names are x_y
        filedict = {}
        for obj in objects:
                tmp_set = set()
                grids = GetGrid(obj['poly'])
                for grid in grids:
                    grid_x, grid_y = grid[0], grid[1]
                    if (grid_x, grid_y) not in tmp_set:
                        leftup_x = math.floor(grid_x * (subsize - gap))
                        leftup_y = math.floor(grid_y * (subsize - gap))
                        rightdown_x = leftup_x + subsize
                        rightdown_y = leftup_y + subsize
                        ## common part
                        polyInsub = self.polyorig2sub(grid, obj['poly'])
                        ## if we don't want the trunated ground truth, set thresh as 1
                        imgpoly = shgeo.Polygon([(leftup_x, leftup_y), (rightdown_x, leftup_y), (rightdown_x, rightdown_y), (leftup_x, rightdown_y)])
                        gtpoly = shgeo.Polygon([(obj['poly'][0], obj['poly'][1]),
                                                 (obj['poly'][2], obj['poly'][3]),
                                                 (obj['poly'][4], obj['poly'][5]),
                                                 (obj['poly'][6], obj['poly'][7])])
                        half_iou = self.calchalf_iou(gtpoly, imgpoly)
                        # print('writing...')
                        outline = ' '.join(list(map(str, polyInsub)))
                        if (obj['difficult']):
                            outline = outline + str(1)
                        ## TODO: find the bug, cause grid_x, grid_y out of index
                        if (half_iou >= self.thresh):
                            if (grid_y > grid_m) or (grid_x > grid_n):
                                #f_error.write(name + '\n')
                                global outlier2
                                outlier2 = outlier2 + 1
                            else:
                                key = str(grid_y) + '_' + str(grid_x)
                                if key not in filedict:
                                    subfilename = outbasename + '-' + key + '.txt'
                                    subdir = os.path.join(self.outlabelpath, subfilename)
                                    filedict[key] = codecs.open(subdir, 'w', 'utf_16')
                                filedict[key].write(outline + '\n')
                                tmp_set.add((grid_x, grid_y))
                        else:
                            global outlier1
                            outlier1 = outlier1 + 1
    def imagesplit(self,
                   img,
                   outbasename,
                   gap,
                   subsize,
                   extent
                   ):
        ## width -- imagesize[1], height -- imagesize[0]
        imagesize = img.shape
        grid_m = int(imagesize[0]/(subsize - gap))
        grid_n = int(imagesize[1]/(subsize - gap))

        ## range are big enough
        for y in range(grid_m + 10):
            for x in range(grid_n + 10):
                index_x1 = int((subsize - gap)*x)
                index_x2 = int(index_x1 + subsize)
                index_y1 = int((subsize - gap)*y)
                index_y2 = int(index_y1 + subsize)

                subimg = np.zeros((subsize, subsize, 3))
                index_x2 = min(index_x2, imagesize[1])
                index_y2 = min(index_y2, imagesize[0])
                sub_width, sub_height = index_x2 - index_x1, index_y2 - index_y1
                subimg[0:sub_height, 0:sub_width] = img[index_y1:index_y2,
                                            index_x1:index_x2]
                subname = outbasename + '-' + str(y) + '_' + str(x) + extent
                subdir = os.path.join(self.outimagepath, subname)
                cv2.imwrite(subdir, subimg)
                if (((x + 1) * (subsize - gap) + gap ) >= imagesize[1]):
                    break
            if (((y + 1) * (subsize - gap) + gap ) >= imagesize[0]):
                break
        #print('<<<<<<<<<<<<<<<<<<<<<<end')

    def SplitSingle(self, name, gap, subsize, rate):
        img = cv2.imread(os.path.join(self.imagepath, name + '.png'))
        if np.shape(img) == ():
            return
        imagesize = img.shape
        resizeimg = cv2.resize(img, None, fx=rate, fy=rate, interpolation = cv2.INTER_CUBIC)
        resizeshape = resizeimg.shape
        outbasename = name + '__' + str(rate) + '__'
        objects = util.parse_bod_poly2(os.path.join(self.labelpath, name + '.txt'))
        for obj in objects:
            obj['poly'] = list(map(lambda x:rate*x, obj['poly']))
        self.imagesplit(resizeimg, outbasename, gap, subsize, '.jpg')
        self.txtsplit(resizeshape, objects, outbasename, gap, subsize)
    def splitdata_half(self, imgenames):
         for name in imgenames:
             self.SplitSingle(name, self.gap, self.subsize, 0.5)
    # def splitdata(filelist, rate, subsize, gap):
    #     for fullname in
    #     SplitSingle()
    def splitdata_2(self, imagenames):
        for name in imagenames:
            self.SplitSingle(name, self.gap, self.subsize, 2)

    def run(self):
        imagelist = GetFileFromThisRootDir(self.imagepath)
        imagenames = [util.mybasename(x) for x in imagelist if (util.mybasename(x) != 'Thumbs')]
        self.splitdata_half(imagenames)
        self.splitdata_2(imagenames)

if __name__ == '__main__':
    split = splitbase(r'E:\bod-dataset',
                      r'E:\bod-dataset\cuttestpath')
    split.run()
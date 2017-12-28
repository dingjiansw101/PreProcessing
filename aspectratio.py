from utils import GetFileFromThisRootDir
import numpy as np
import os
import utils as util
import codecs
import pickle
import matplotlib.pyplot as plt
from operations import filecopy



def distance(point1, point2):
    return np.sqrt(np.sum(np.square(point1 - point2)))

# ratio_ranges = [(0.2, 0.6799999999999999), (0.6799999999999999, 1.16), (1.16, 1.64), (1.64, 2.12), (2.12, 2.6), (2.6, 3.08), (3.08, 3.56), (3.56, 4.04), (4.04, 4.5200000000000005), (4.5200000000000005, 5.0)]
# yvalues_rec = [706.0, 44999.0, 80872.0, 30146.0, 15520.0, 8238.0, 4357.0, 1594.0, 874.0, 461.0, 276.0, 842.0]
# yvalues_rot = [10877.0, 139265.0, 25417.0, 6751.0, 2610.0, 1345.0, 518.0, 376.0, 359.0, 401.0, 357.0, 609.0]

ratio_ranges = [(0, 0.2), (0.2, 0.44), (0.44, 0.6799999999999999), (0.6799999999999999, 0.9199999999999999), (0.9199999999999999, 1.16), (1.16, 1.4), (1.4, 1.64), (1.64, 1.88), (1.88, 2.12), (2.12, 2.3600000000000003), (2.3600000000000003, 2.6), (2.6, 2.84), (2.84, 3.08), (3.08, 3.3200000000000003), (3.3200000000000003, 3.56), (3.56, 3.8), (3.8, 4.04), (4.04, 4.28), (4.28, 4.5200000000000005), (4.5200000000000005, 4.76), (4.76, 5.0)]
yvalues_rec = [1602.0, 18499.0, 35804.0, 43033.0, 35193.0, 16100.0, 10615.0, 7652.0, 6180.0, 4239.0, 3395.0, 1941.0, 1279.0, 714.0, 594.0, 356.0, 333.0, 209.0, 180.0, 125.0, 842.0]
yvalues_rot_best = [13227.0, 58799.0, 15630.0, 12425.0, 12323.0, 3974.0, 3313.0, 6262.0, 10306.0, 10231.0, 9316.0, 7479.0, 5131.0, 3313.0, 2523.0, 2232.0, 2145.0, 1787.0, 1529.0, 1131.0, 5809.0]
names = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75]
yvalues_rot = [23772.0, 105031.0, 23626.0, 13716.0, 11079.0, 3859.0, 1886.0, 1246.0, 1282.0, 583.0, 369.0, 255.0, 209.0, 202.0, 175.0, 194.0, 217.0, 202.0, 211.0, 162.0, 609.0]
def plotbar_size(names, yvalues):
    ind = np.arange(len(yvalues))  # the x locations for the groups
    width = 0.8  # the width of the bars: can also be len(x) sequence
    plt.bar(ind, yvalues, width, color='#0000FF')
    plt.ylabel('number of each aspect ratio')
    plt.xlabel('aspect ratio')
    #    plt.title('size distribution of plane ()')

    ind2 = np.arange(len(names))
    # names = list(map(float, names))
    plt.xticks(ind2, names, rotation=45, fontsize='small')

    plt.ylim(ymin=0)
    # plt.xlim(xmin=0, xmax=self.barnum)
    plt.xlim(xmin=0)
    plt.show()

def getallbodar_rec():
    filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\wordlabel')
    ratios = []
    for fullname in filelist:
        objects = util.parse_bod_rec(fullname)
        for obj in objects:
            bbox = obj['bndbox']
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            ratio = float(w) / float(h)
            ratios.append(ratio)
    return ratios
def getallobdar_rot():
    filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\wordlabel')
    ratios = []
    for fullname in filelist:
        objects = util.parse_bod_poly(fullname)
        for obj in objects:
            poly = obj['poly']
            poly = list(map(lambda x: np.array(x), poly))
            len1 = distance(poly[0], poly[1])
            len2 = distance(poly[1], poly[2])
            ratio = float(len1) / float(len2)
            ratios.append(ratio)
    return  ratios

def generaterangenum(ratios):
     min_ratio = 0
     max_ratio = 5
     interval_num = 20
     gap = (max_ratio - min_ratio) / interval_num
     ## generate ranges
#     ranges = [(min_ratio + x * gap, min_ratio + (x + 1) * gap) for x in range(interval_num)]
     names = [x * gap for x in range(interval_num)]
     yvalues = np.zeros(interval_num + 1)
     for ratio in ratios:
         index = int( (ratio - min_ratio) / gap )
         if (index > interval_num):
             index = interval_num
         yvalues[index] = yvalues[index] + 1
     return yvalues

def test_generaterangenum():
    ratios = [0.1, 0.3, 0.5, 0.7, 0.8, 4.8, 5.1]
    yvalues = generaterangenum(ratios)
    print(list(yvalues))
def count_rec():
    ratios = getallbodar_rec()
    yvalues = generaterangenum(ratios)
    print(list(yvalues))

def count_rot():
    ratios = getallobdar_rot()
    yvalues = generaterangenum(ratios)
    print(list(yvalues))
if __name__ == '__main__':
    # count_rec()
    # count_rot()
    #test_generaterangenum()
    plotbar_size(names, yvalues_rot)
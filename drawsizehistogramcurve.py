import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import utils as util
import pickle
import os

# top = [  2.76940000e+04   5.65480000e+04   4.95800000e+04   1.58230000e+04
#    1.10320000e+04   8.31800000e+03   3.69100000e+03   2.62200000e+03
#    2.07800000e+03   1.77000000e+03   2.01300000e+03   1.83100000e+03
#    1.12400000e+03   7.15000000e+02   4.89000000e+02   3.34000000e+02
#    3.75000000e+02   3.06000000e+02   2.66000000e+02   2.57000000e+02
#    2.41000000e+02   2.19000000e+02   1.49000000e+02   1.44000000e+02
#    1.20000000e+02   1.29000000e+02   1.09000000e+02   7.60000000e+01
#    7.40000000e+01   7.50000000e+01   6.20000000e+01   6.30000000e+01
#    3.60000000e+01   4.10000000e+01   3.40000000e+01   3.80000000e+01
#    2.90000000e+01   2.60000000e+01   2.80000000e+01   2.10000000e+01
#    2.20000000e+01   2.30000000e+01   2.60000000e+01   1.50000000e+01
#    1.80000000e+01   1.20000000e+01   1.40000000e+01   1.60000000e+01
#    1.00000000e+01   5.00000000e+00   1.20000000e+01   1.20000000e+01
#    1.20000000e+01   5.00000000e+00   4.00000000e+00   4.00000000e+00
#    5.00000000e+00   7.00000000e+00   8.00000000e+00   7.00000000e+00
#    3.00000000e+00   3.00000000e+00   5.00000000e+00   4.00000000e+00
#    2.00000000e+00   3.00000000e+00   0.00000000e+00   4.00000000e+00
#    0.00000000e+00   0.00000000e+00   1.00000000e+00   4.00000000e+00
#    4.00000000e+00   3.00000000e+00   4.00000000e+00   1.00000000e+00
#    0.00000000e+00   2.00000000e+00   2.00000000e+00   0.00000000e+00
#    6.00000000e+00   0.00000000e+00   1.00000000e+00   2.00000000e+00
#    1.00000000e+00   0.00000000e+00   1.00000000e+00   0.00000000e+00
#    1.00000000e+00   1.00000000e+00   3.00000000e+00   1.00000000e+00
#    0.00000000e+00   1.00000000e+00   0.00000000e+00   0.00000000e+00
#    1.00000000e+00   2.00000000e+00   1.00000000e+00   1.00000000e+00]
outleft = [3.0,20.47,37.94,55.41,72.88,90.35,107.82,125.29,142.76,160.23,177.7,
           195.17,212.64,230.11,247.58,265.05,282.52,299.99,317.46,334.93,352.4,369.87,387.34,404.81,422.28,439.75,457.22,474.69,492.16,509.63,527.1,544.57,562.04,579.51,596.98,614.45,631.92,649.39,666.86,684.33,701.8,719.27,736.74,754.21,771.68,789.15,806.62,824.09,841.56,859.03,876.5,893.97,911.44,928.91,946.38,963.85,981.32,998.79,1016.26,1033.73,1051.2,1068.67,1086.14,1103.61,1121.08,1138.55,1156.02,1173.49,1190.96,1208.43,1225.9,1243.37,1260.84,1278.31,1295.78,1313.25,1330.72,1348.19,1365.66,1383.13,1400.6,1418.07,1435.54,1453.01,1470.48,1487.95,1505.42,1522.89,1540.36,1557.83,1575.3,1592.77,1610.24,1627.71,1645.18,1662.65,1680.12,1697.59,1715.06,1732.53]
outbins = [3.0,20.47,37.94,55.41,72.88,90.35,107.82,125.29,142.76,160.23,177.7,195.17,212.64,230.11,247.58,265.05,282.52,299.99,317.46,334.93,352.4,369.87,387.34,404.81,422.28,439.75,457.22,474.69,492.16,509.63,527.1,544.57,562.04,579.51,596.98,614.45,631.92,649.39,666.86,684.33,701.8,719.27,736.74,754.21,771.68,789.15,806.62,824.09,841.56,859.03,876.5,893.97,911.44,928.91,946.38,963.85,981.32,998.79,1016.26,1033.73,1051.2,1068.67,1086.14,1103.61,1121.08,1138.55,1156.02,1173.49,1190.96,1208.43,1225.9,1243.37,1260.84,1278.31,1295.78,1313.25,1330.72,1348.19,1365.66,1383.13,1400.6,1418.07,1435.54,1453.01,1470.48,1487.95,1505.42,1522.89,1540.36,1557.83,1575.3,1592.77,1610.24,1627.71,1645.18,1662.65,1680.12,1697.59,1715.06,1732.53,1750.0]
def distance(point1, point2):
    return np.sqrt(np.sum(np.square(point1 - point2)))

def drawhistogram(data, ax):

    n, bins = np.histogram(data, 100, )

    print('len bins:', len(bins))
    print('bins:', bins)

    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + n
    print('left:', left)
    print('right:', right)
    print('bottom:', bottom)
    print('top:', top)

    # we need a (numrects x numsides x 2) numpy array for the path helper
    # function to build a compound path
    XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

    # get the Path object
    barpath = path.Path.make_compound_path_from_polys(XY)
    patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='black')
    # make a patch out of it
    #patch = patches.PathPatch(barpath)
    ax.add_patch(patch)
    #plt.yscale('log')
    # update the view limits
    ax.set_yscale('log')
    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max())

    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(16)

    ## set the font for x label
    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(16)
#
# def picklewrap(func, classname, filename):
#     if os.path.exists(filename):
#         with open(filename, 'rb') as f:
#             sizes = pickle.load(f)
#     else:


def getsizes(classname):
    filslist = util.GetFileFromThisRootDir(r'E:\bod-dataset\wordlabelBestStart')
    sizes = []
    for fullname in filslist:
        objects = util.parse_bod_rec(fullname)
        for obj in objects:
            w, h = obj['bndbox'][2] - obj['bndbox'][0], obj['bndbox'][3] - obj['bndbox'][1]
            size = h
            if obj['name'] == classname:
                sizes.append(size)
    return sizes

def getsizesall():
    filslist = util.GetFileFromThisRootDir(r'E:\bod-dataset\wordlabelBestStart')
    sizes = []
    for fullname in filslist:
        objects = util.parse_bod_rec(fullname)
        for obj in objects:
            w, h = obj['bndbox'][2] - obj['bndbox'][0], obj['bndbox'][3] - obj['bndbox'][1]
            size = h
            sizes.append(size)
    return sizes

def drawhistogram_curve(data, ax):
    n, bins = np.histogram(data, 100)

    print('len bins:', len(bins))
    print('bins:', bins)
    outbins = ','.join(map(str, bins))
    print('outbins:', outbins)
    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + n
    print('left:', left)
    print('right:', right)
    print('bottom:', bottom)
    print('top:', top)

    outleft = ','.join(map(str, left))
    print('outleft:', outleft)
    ax.plot(left, top)
    ax.set_yscale('log')
    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max())

def plotsize_all():
    sizes = getsizesall()
    fig, ax = plt.subplots()
    drawhistogram_curve(sizes, ax)
    plt.xlabel('size of '+ 'pixel', fontsize='xx-large')
    plt.ylabel('frequency', fontsize='xx-large')
    plt.show()

if __name__ == '__main__':

    plotsize_all()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import utils as util
import pickle
import os
import codecs


def distance(point1, point2):
    return np.sqrt(np.sum(np.square(point1 - point2)))

def drawhistogram(data, ax):

    n, bins = np.histogram(data, 30)
    print('len bins:', len(bins))

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

    # make a patch out of it
    patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='black')
    ax.add_patch(patch)
    #plt.yscale('log')
    # update the view limits
    ax.tick_params(axis='y', labelsize='x-large')
    ax.tick_params(axis='x', labelsize='xx-large')
    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max())

def getallbodar_rec():
    filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\wordlabel')
    ratios = []
    picklepath = r'E:\bod-dataset\pickle\ratios_rec.pickle'
    if (os.path.exists(picklepath)):
        with open(picklepath, 'rb') as f:
            ratios = pickle.load(f)
    else:
        for fullname in filelist:
            objects = util.parse_bod_rec(fullname)
            for obj in objects:
                bbox = obj['bndbox']
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                ratio = float(w) / float(h)
                ratios.append(ratio)
        with open(picklepath, 'wb') as f:
            pickle.dump(ratios, f, pickle.HIGHEST_PROTOCOL)

    return ratios
def getallobdar_rot():
    filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\wordlabel')
    ratios = []
    picklepath = r'E:\bod-dataset\pickle\ratios_rot.pickle'
    if (os.path.exists(picklepath)):
        with open(picklepath, 'rb') as f:
            ratios = pickle.load(f)
    else:
        for fullname in filelist:
            objects = util.parse_bod_poly(fullname)
            for obj in objects:
                poly = obj['poly']
                poly = list(map(lambda x: np.array(x), poly))
                len1 = distance(poly[0], poly[1])
                len2 = distance(poly[1], poly[2])
                ratio = float(len1) / float(len2)
                #if (ratio < 17):
                ratios.append(ratio)
        with open(picklepath, 'wb') as f:
            pickle.dump(ratios, f, pickle.HIGHEST_PROTOCOL)
    return  ratios
def getallobdar_rot2():
    filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\wordlabelBestStart')
    ratios = []
    picklepath = r'E:\bod-dataset\pickle\ratios_rot2.pickle'
    if (os.path.exists(picklepath)):
        with open(picklepath, 'rb') as f:
            ratios = pickle.load(f)
            return ratios
    for fullname in filelist:
        objects = util.parse_bod_poly(fullname)
        for obj in objects:
            poly = obj['poly']
            poly = list(map(lambda x: np.array(x), poly))
            len1 = distance(poly[0], poly[1])
            len2 = distance(poly[1], poly[2])
            ratio = float(len1) / float(len2)
            ratios.append(ratio)
    with open(picklepath, 'wb') as f:
        pickle.dump(ratios, f, pickle.HIGHEST_PROTOCOL)
    return  ratios

def getinstances():
    filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\wordlabelBestStart')
    instances = []
    picklepath = r'E:\bod-dataset\pickle\instances.pickle'
    if (os.path.exists(picklepath)):
        with open(picklepath, 'rb') as f:
            instances = pickle.load(f)
            return instances
    for fullname in filelist:
        with codecs.open(fullname, 'r', 'utf_16') as f:
            lines = f.readlines()
            num = len(lines)
            instances.append(num)
    with open(picklepath, 'wb') as f:
        pickle.dump(instances, f, pickle.HIGHEST_PROTOCOL)
    return  instances
def drawAR():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    ratios_rec = list(filter(lambda x: x < 6, getallbodar_rec()))
#    ratios_rot = list(filter(lambda x: x < 20, getallobdar_rot()))
    ratios_rot = list(filter(lambda x: x < 6, getallobdar_rot2()))

    instances = list(filter(lambda x: x < 1700, getinstances()))
    ax1.set_ylabel('#Instances', fontsize='20')
    ax1.set_xlabel('AR of horizontal bounding box', fontsize='20')
    ax1.set_yscale('log')

    ax2.set_ylabel('#Instances', fontsize='20')
    ax2.set_xlabel('AR of oriented bounding box', fontsize='20')
    ax2.set_yscale('log')

    ax3.set_ylabel('#Images', fontsize='20')
    ax3.set_xlabel('Number of Instances', fontsize='20')
    ax3.set_yscale('log')

    drawhistogram(ratios_rec, ax1)

    drawhistogram(ratios_rot, ax2)

    drawhistogram(instances, ax3)
    plt.show()
if __name__ == '__main__':
    drawAR()
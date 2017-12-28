import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import utils as util
import pickle
import os


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

    outtop = ','.join(map(str, top))
    print('outtop:', outtop)

    outleft = ','.join(map(str, left))
    print('outleft:', outleft)

    # we need a (numrects x numsides x 2) numpy array for the path helper
    # function to build a compound path
    XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

    # get the Path object
    barpath = path.Path.make_compound_path_from_polys(XY)
    patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='white')
    # make a patch out of it
    #patch = patches.PathPatch(barpath)
    ax.add_patch(patch)
    #plt.yscale('log')
    # update the view limits
    ax.set_yscale('log')
    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max())

    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(18)

    ## set the font for x label
    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(18)
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
def plotsize_all():
    sizes = getsizesall()
    fig, ax = plt.subplots()
    drawhistogram(sizes, ax)
    plt.xlabel('size of '+ 'pixel', fontsize='xx-large')
    plt.ylabel('frequency', fontsize='xx-large')
    plt.show()
selectedname = ['bridge', 'ground-track-field', 'harbor', 'helicopter', 'small-vehicle', 'large-vehicle',
                'ship', 'plane']
if __name__ == '__main__':
    # fig, axes = plt.subplots(2, 4)
    # for index, classname in enumerate(selectedname):
    #     sizes = getsizes(classname)
    #     x = int(index/4)
    #     y = index%4
    #     print('x:', x)
    #     print('y:', y)
    #     print('axes:', axes)
    #     if (classname == 'ship'):
    #         sizes = list(filter(lambda x: x < 750, sizes))
    #     drawhistogram(sizes, axes[x, y])
    #     axes[x, y].set_xlabel('size of '+ str(classname + '(pixel)'))
    #     if (y == 0):
    #         axes[x, y].set_ylabel('frequency')
    # plt.show()
    plotsize_all()
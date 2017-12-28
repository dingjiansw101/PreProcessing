import utils as util
import os
import codecs
import re
import xml.etree.ElementTree as ET
import math
import numpy as np

nwpudict = {'plane': 757, 'ship': 302, 'storage-tank': 655, 'baseball-diamond': 390,
            'tennis-court': 524, 'basketball-court': 159, 'ground-track-field': 163,
            'harbor': 224, 'bridge': 124, 'small-vehicle': 598}

boddict = {'plane': 14085, 'ship': 52516, 'storage-tank': 11794, 'baseball-diamond': 1130,
           'tennis-court': 4654, 'basketball-court': 954, 'ground-track-field': 678,
           'harbor': 12287, 'bridge': 3760, 'small-vehicle': 48891, 'large-vehicle': 31613,
           'turntable': 871, 'swimming-pool': 3507, 'helicopter': 822, 'soccer-ball-field': 720}

import matplotlib.pyplot as plt


def comparewithnwpu():
    N = 15
    classnames = [x for x in boddict]
    print('classnames: ', classnames)
    nwpunums = np.ones(15)
    width = 0.35
    for key in nwpudict:
        index = classnames.index(key)
        nwpunums[index] = nwpudict[key]
    bodnums = np.array([(boddict[classnames[i]] - nwpunums[i]) for i in range(N)])
    ind = np.arange(N)

    nwpunums = (757, 302, 655, 390, 524, 159, 163, 224, 124, 598, 1, 1, 1, 1, 1)
    bodnums = (14490, 52699, 11159, 745, 4222, 812, 521, 12461, 3661, 48923, 32619, 877, 3612, 844, 722)

    p1 = plt.bar(ind, nwpunums, width)
    p2 = plt.bar(ind, bodnums, width, bottom=nwpunums)

    plt.ylabel('Number of instances')
    plt.title('Instances per category')
    plt.xticks(ind, classnames, rotation=45, fontsize='small')
    plt.yticks(np.arange(0, 81, 10))
    plt.yscale('log')
    plt.ylim(ymin=100)
    plt.legend((p1[0], p2[0]), ('NWPU VHR 10', 'BOD'))

    plt.show()

def example():
    N = 5
    menMeans = (20, 35, 0, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    menStd = (2, 3, 4, 1, 2)
    womenStd = (3, 5, 2, 3, 3)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, menMeans, width)
    p2 = plt.bar(ind, womenMeans, width,
                 bottom=menMeans)

    plt.ylabel('Scores')
    plt.title('Scores by group and gender')
    plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.yticks(np.arange(0, 81, 10))
    plt.legend((p1[0], p2[0]), ('Men', 'Women'))

    plt.show()
if __name__ == '__main__':
    comparewithnwpu()
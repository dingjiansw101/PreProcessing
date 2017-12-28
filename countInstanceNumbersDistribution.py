import utils as util
import os
import numpy as np
from plot import plotbar_instances
import matplotlib.pyplot as plt

maxn_instances = 2000
gap_bar = np.int(100)
gap_value = np.int(100)
imagenumbers_instance = np.zeros(int(maxn_instances/gap_value) + 1)
names = [str(gap_value*x) for x in range(int(maxn_instances/gap_value))]

def countNumber(path):
    #labelpath = os.path.join(path, 'labelTxt')
    labelpath = os.path.join(path, 'wordlabel')
    filelist = util.GetFileFromThisRootDir(labelpath)
    for fullname in filelist:
        f = open(fullname, 'r', encoding='utf-16')
        lines = f.readlines()
        instanceNumber = len(lines)
        index = int(instanceNumber/gap_bar)
        imagenumbers_instance[index] = imagenumbers_instance[index] + 1
def countInstanceNumbers():
    basepath = r'E:\bod-dataset'
    # testpath = os.path.join(basepath, 'testsplit')
    # trainpath = os.path.join(basepath, 'trainsplit-2')
    #countNumber(testpath)
    #countNumber(trainpath)

    countNumber(basepath)
    yvalues = list(imagenumbers_instance)
    mult = gap_value/gap_bar
    savefigpath = r'E:\documentation\dataset\aerial_detection_dataset\images\instanceDistribution.png'

    plotbar_instances(names, yvalues, mult, savefigpath)

if __name__ == '__main__':
    countInstanceNumbers()
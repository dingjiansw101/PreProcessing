import matplotlib.pyplot as plt
import os
import numpy as np
from io import BytesIO
# return locs, labels where locs is an array of tick locations and
# labels is an array of tick labels.


def plotbar(names, yvalues, fname='', suffix='png'):
    ind = np.arange(len(yvalues))  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence
    plt.bar(ind, yvalues, width, color='#d62728')
    plt.ylabel('number of each category')
    plt.title('categories')
    plt.xticks(ind, names, rotation=45, fontsize='small')
    plt.yticks(np.arange(0, 81, 10))
    plt.yscale('log')
    plt.ylim(ymin=100)
    if fname != '':
        plt.savefig(fname)
    plt.show()

def plotbar_instances(names, yvalues, mult, fname='', suffix='eps'):
    ind = np.arange(len(yvalues))  # the x locations for the groups
    width = 0.8  # the width of the bars: can also be len(x) sequence
    plt.bar(ind + width/2, yvalues, width, color='#0000FF')
    plt.ylabel('Number of images', fontsize='xx-large')
    plt.xlabel('Instances', fontsize='xx-large')
#    plt.title('size distribution of plane ()')
    plt.tick_params(labelsize=20)
    ind2 = mult*np.arange(len(names))
    plt.xticks(ind2, names, rotation=45)
    #plt.yticks(np.arange(0, 1000, 10))
    plt.yscale('log')
    plt.ylim(ymin=0.1)
    plt.xlim(xmin=0, xmax=len(yvalues))
    if fname != '':
        plt.savefig(fname)
    plt.show()


def plotbar_size(names, yvalues, fname='', suffix='png'):
    ind = np.arange(len(yvalues))  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence
    plt.bar(ind, yvalues, width, color='#d62728')
    plt.ylabel('number of each category')
    plt.title('categories')
    plt.xticks(ind, names, rotation=45, fontsize='small')
    plt.yticks(np.arange(0, 81, 10))
    #plt.yscale('log')
    plt.ylim(ymin=10)
    plt.savefig(fname)
    plt.show()
def testplotbar():
    names = ('G1', 'G2', 'G3', 'G4', 'G5')
    yvalues = (10, 100, 300, 1000, 3000)
    plotbar(names, yvalues)

def plotNumberDistribution():
    pass
if __name__ == '__main__':
    testplotbar()
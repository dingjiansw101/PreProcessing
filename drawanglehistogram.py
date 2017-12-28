import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import utils as util
import pickle
import os
import math

anglenums = [-3.14032361874,-3.07750445601,-3.01468529329,-2.95186613057,-2.88904696784,-2.82622780512,-2.7634086424,-2.70058947968,-2.63777031695,-2.57495115423,-2.51213199151,-2.44931282878,-2.38649366606,-2.32367450334,-2.26085534061,-2.19803617789,-2.13521701517,-2.07239785244,-2.00957868972,-1.946759527,-1.88394036427,-1.82112120155,-1.75830203883,-1.6954828761,-1.63266371338,-1.56984455066,-1.50702538793,-1.44420622521,-1.38138706249,-1.31856789976,-1.25574873704,-1.19292957432,-1.13011041159,-1.06729124887,-1.00447208615,-0.941652923423,-0.8788337607,-0.816014597977,-0.753195435253,-0.69037627253,-0.627557109807,-0.564737947084,-0.50191878436,-0.439099621637,-0.376280458914,-0.313461296191,-0.250642133467,-0.187822970744,-0.125003808021,-0.0621846452974,0.000634517425878,0.0634536801492,0.126272842872,0.189092005596,0.251911168319,0.314730331042,0.377549493766,0.440368656489,0.503187819212,0.566006981935,0.628826144659,0.691645307382,0.754464470105,0.817283632828,0.880102795552,0.942921958275,1.005741121,1.06856028372,1.13137944644,1.19419860917,1.25701777189,1.31983693461,1.38265609734,1.44547526006,1.50829442278,1.57111358551,1.63393274823,1.69675191095,1.75957107368,1.8223902364,1.88520939912,1.94802856185,2.01084772457,2.07366688729,2.13648605002,2.19930521274,2.26212437546,2.32494353819,2.38776270091,2.45058186363,2.51340102636,2.57622018908,2.6390393518,2.70185851453,2.76467767725,2.82749683997,2.8903160027,2.95313516542,3.01595432814,3.07877349087]

angles = [-3.14032361874,-3.07750445601,-3.01468529329,-2.95186613057,-2.88904696784,-2.82622780512,-2.7634086424,-2.70058947968,-2.63777031695,-2.57495115423,-2.51213199151,-2.44931282878,-2.38649366606,-2.32367450334,-2.26085534061,-2.19803617789,-2.13521701517,-2.07239785244,-2.00957868972,-1.946759527,-1.88394036427,-1.82112120155,-1.75830203883,-1.6954828761,-1.63266371338,-1.56984455066,-1.50702538793,-1.44420622521,-1.38138706249,-1.31856789976,-1.25574873704,-1.19292957432,-1.13011041159,-1.06729124887,-1.00447208615,-0.941652923423,-0.8788337607,-0.816014597977,-0.753195435253,-0.69037627253,-0.627557109807,-0.564737947084,-0.50191878436,-0.439099621637,-0.376280458914,-0.313461296191,-0.250642133467,-0.187822970744,-0.125003808021,-0.0621846452974,0.000634517425878,0.0634536801492,0.126272842872,0.189092005596,0.251911168319,0.314730331042,0.377549493766,0.440368656489,0.503187819212,0.566006981935,0.628826144659,0.691645307382,0.754464470105,0.817283632828,0.880102795552,0.942921958275,1.005741121,1.06856028372,1.13137944644,1.19419860917,1.25701777189,1.31983693461,1.38265609734,1.44547526006,1.50829442278,1.57111358551,1.63393274823,1.69675191095,1.75957107368,1.8223902364,1.88520939912,1.94802856185,2.01084772457,2.07366688729,2.13648605002,2.19930521274,2.26212437546,2.32494353819,2.38776270091,2.45058186363,2.51340102636,2.57622018908,2.6390393518,2.70185851453,2.76467767725,2.82749683997,2.8903160027,2.95313516542,3.01595432814,3.07877349087,3.14159265359]


def distance(point1, point2):
    return np.sqrt(np.sum(np.square(point1 - point2)))

def drawhistogram(data, ax):

    n, bins = np.histogram(data, 100)

    print('len bins:', len(bins))
    outbins = ','.join(map(str, bins))
    print('outbins: ', outbins)
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
    outtop = ','.join(map(str, top))
    print('outtop:', outtop)
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

def getangleall():
    filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\wordlabel')
    angles = []
    for fullname in filelist:
        objects = util.parse_bod_poly(fullname)
        for obj in objects:
            poly = obj['poly']
            x2, y2 = poly[1][0], poly[1][1]
            x3, y3 = poly[2][0], poly[2][1]
            angle = math.atan2(y3 - y2, x3 - x2)
            angles.append(angle)
    return  angles
def plotangle_all():
    sizes = getangleall()
    fig, ax = plt.subplots()
    drawhistogram(sizes, ax)
    plt.xlabel('angles', fontsize='xx-large')
    plt.ylabel('frequency', fontsize='xx-large')
    plt.show()

if __name__ == '__main__':

    plotangle_all()
from utils import GetFileFromThisRootDir
import numpy as np
import os
import utils as util
import codecs
from plot import plotbar_size
import pickle
import matplotlib.pyplot as plt
from operations import filecopy



## TODO find the small-vehicle, large-vehicle outlier, some small-vehicle is larger than larger vehicle!!!!
class SizeDistribution(object):
    def __init__(self,
                 basepath):
        self.classs_physic = {'ground-track-field': [], 'small-vehicle': [], 'large-vehicle': [], 'harbor': [], 'plane': [], 'ship': [],
                      'basketball-court': [], 'swimming-pool': [], 'helicopter': [], 'bridge': [], 'tennis-court': [],
                      'baseball-diamond': [], 'storage-tank': [], 'soccer-ball-field': [], 'turntable': [],
                      }
        self.classs_pixel = {'ground-track-field': [], 'small-vehicle': [], 'large-vehicle': [], 'harbor': [], 'plane': [], 'ship': [],
                      'basketball-court': [], 'swimming-pool': [], 'helicopter': [], 'bridge': [], 'tennis-court': [],
                      'baseball-diamond': [], 'storage-tank': [], 'soccer-ball-field': [], 'turntable': [],
                      }

        #self.usual_range = {'ground-track-field': (0, 270), 'small-vehicle': (0, 13), 'large-vehicle': (0, 30), 'harbor': (0, 350), 'plane': (0, 110),
         #                   'basketball-court': (0, 50), 'swimming-pool': (0,70), 'tennis-court': (10, 50), 'baseball-diamond': (0, 80),
          #                  'soccer-ball-field': (0, 130), 'turntable': (0, 110)}
        self.usual_range = {'ground-track-field': (0, 270), 'small-vehicle': (0, 13), 'large-vehicle': (0, 30), 'harbor': (0, 350), 'plane': (0, 110),
                            'basketball-court': (0, 50), 'swimming-pool': (0,70), 'tennis-court': (10, 50), 'baseball-diamond': (0, 80),
                            'soccer-ball-field': (0, 130), 'turntable': (0, 110)}
        self.selectedname = ['bridge', 'ground-track-field', 'harbor', 'helicopter', 'small-vehicle', 'large-vehicle',
                'ship', 'plane']
        self.namedict = {'ground-track-field': 'ground track field', 'small-vehicle': 'small vehicle',
                         'large-vehicle': 'large vehicle', 'basketball-court': 'basketball court', 'swimming-pool': 'swimming pool',
                         'tennis-court': 'tennis court', 'baseball-diamond': 'basball diamond', 'soccer-ball-field': 'soccer ball field'}
        self.basepath = basepath
        self.respath = os.path.join(self.basepath, 'resolution')
        self.imgpath = os.path.join(self.basepath, 'images')
        self.labelpath = os.path.join(self.basepath, 'wordlabel')
        self.barnum = 28
        self.xname_num = 8
        self.picklepath = os.path.join(self.basepath, 'pickle')
        self.debugpath = r'E:\bod-dataset\datadebug'
        self.bugnames = []
        self.bugfilelist = r'E:\bod-dataset\datadebug\bug.txt'
        self.f_bug = open(self.bugfilelist, 'w')
        #self.sizeAnalysis('physic')
        if not os.path.exists(os.path.join(self.picklepath, 'physic.pickle')):
            self.sizeAnalysis('physic')
            with open(os.path.join(self.picklepath, 'physic.pickle'), 'wb') as f:
                pickle.dump(self.classs_physic, f, pickle.HIGHEST_PROTOCOL)
        else:
            with open(os.path.join(self.picklepath, 'physic.pickle'), 'rb') as f:
                self.classs_physic = pickle.load(f)

        if not os.path.exists(os.path.join(self.picklepath, 'pixel.pickle')):
            self.sizeAnalysis('pixel')
            with open(os.path.join(self.picklepath, 'pixel.pickle'), 'wb') as f:
                pickle.dump(self.classs_pixel, f, pickle.HIGHEST_PROTOCOL)
        else:
            with open(os.path.join(self.picklepath, 'pixel.pickle'), 'rb') as f:
                self.classs_pixel = pickle.load(f)

    def __del__(self):
        self.f_bug.close()
        pass
    def getresolution(self, name):
        resname = os.path.join(self.respath, name + '.txt')
        with open(resname, 'r') as f:
            line = f.readline()
            resolution = line.strip()
            #if float(resolution) < 0.1:
             #   print('reaname: ', resname)
        return resolution

    def plotbar_size(self, names, yvalues, category, xmin, xmax, fname='', suffix='.eps', type='physic'):

        ind = np.arange(len(yvalues))  # the x locations for the groups
        print ('xmin:', xmin)
        print ('xmax:', xmax)
        gap = int((float(xmax) - float(xmin)) / self.xname_num)
        width = 0.6  # the width of the bars: can also be len(x) sequence
        #ind = ind + 0.5
        rect = plt.bar(ind + width/2, yvalues, width, color='#0000FF')
        plt.ylabel('frequency', fontsize='large')
        #plt.xlabel('size of ' + category)
        #    plt.title('size distribution of plane ()')
        plt.xlabel('size of pixel', fontsize='large')
        ind2 = self.barnum/self.xname_num * np.arange(len(names))
        #names = list(map(float, names))
        if category in self.namedict:
            category = self.namedict[category]
        plt.legend((rect,), (str(category), ), fontsize='large')
        plt.xticks(ind2, names, fontsize='16')
        # plt.yticks(np.arange(0, 1000, 10))
        plt.yscale('log')
        plt.ylim(ymin=1)

       # plt.xlim(xmin=0, xmax=self.barnum)
        plt.xlim(xmin=0, xmax=self.barnum)
        if fname != '':
             plt.savefig(fname)
        plt.show()
    def plotbar_size_ax(self, ax, names, yvalues, category, xmin, xmax):

        ind = np.arange(len(yvalues))  # the x locations for the groups
        print ('xmin:', xmin)
        print ('xmax:', xmax)
        gap = int((float(xmax) - float(xmin)) / self.xname_num)
        width = 0.6  # the width of the bars: can also be len(x) sequence
        #ind = ind + 0.5
        rect = ax.bar(ind + width/2, yvalues, width, color='#0000FF')
        ax.set_ylabel('frequency', fontsize='large')
        #plt.xlabel('size of ' + category)
        #    plt.title('size distribution of plane ()')
        ax.set_xlabel('size of pixel', fontsize='large')
        ind2 = self.barnum/self.xname_num * np.arange(len(names))
        #names = list(map(float, names))
        if category in self.namedict:
            category = self.namedict[category]
        ax.legend((rect,), (str(category), ), fontsize='large')
        ax.set_xticks(ind2)
        ax.set_xticklabels(names)
        ax.tick_params(labelsize=16)
        # plt.yticks(np.arange(0, 1000, 10))
        ax.set_yscale('log')
        #plt.ylim(ymin=1)

       # plt.xlim(xmin=0, xmax=self.barnum)
#        plt.xlim(xmin=0, xmax=self.barnum)

    def sizeAnalysis(self, type='physic'):
        filelist = GetFileFromThisRootDir(self.imgpath)
        for fullname in filelist:
            if 'Thumbs' in fullname:
                continue
            name = util.mybasename(fullname)

            resolution = self.getresolution(name)
            if (resolution == ''):
                continue

            if float(resolution) < 0.1:
                continue
#            print('resolution:', resolution)
 #           print('type resolution:', resolution)
            #print 'resolution:', resolution

            resolution = float(resolution)
            labelname = os.path.join(self.labelpath, name + '.txt')
            objects = util.parse_bod_poly(labelname)
            for obj in objects:
                assert obj['name'] in self.classs_pixel, 'the name is not in 15 classes'
                wordname = obj['name']
                if type == 'physic':
                    lenth = resolution * obj['long-axis']
                    #if (wordname == 'small-vehicle'):
                       # assert lenth <= 15, 'the small-vehicle should shorter than 15, ' + 'wrong imgname is ' + fullname
                    if wordname in self.usual_range:
                        lenth_range = self.usual_range[wordname]
                        if (lenth < lenth_range[0]) or (lenth > lenth_range[1]):
                            #print('bug name:', name)
                            #print('bug category:', wordname)
                            outline = name + ' ' + wordname
                            #self.f_bug.write(outline + '\n')
                            if name not in self.bugnames:
                                self.bugnames.append(name)

                    self.classs_physic[wordname].append(lenth)
                elif type == 'pixel':
                    lenth = obj['long-axis']
                    #if (obj['name'] == 'ground-track-field'):
                        #assert lenth > 30, str(name) + 'has something wrong'
                    self.classs_pixel[wordname].append(lenth)
                ## 2 is the gap between
    def generateplotX_Y(self, class_name, flag='physic'):
        lengths = []
        if (flag == 'physic'):
            lengths = self.classs_physic[class_name]
        elif (flag == 'pixel'):
            lengths = self.classs_pixel[class_name]
        len_min = min(lengths)
        len_max = max(lengths)
        print('class_name:', class_name)
        print ('type len_min:', type(len_min))
        print ('len_min:', len_min)
        print ('len_max:', len_max)
        name_gap = (len_max - len_min) / self.xname_num
        X_names = name_gap * np.arange(self.xname_num)
        X_names = list(map(int, X_names))
        X_names = list(map(str, X_names))
        Y_gap = (len_max - len_min) / self.barnum
        yvalues = np.zeros(self.barnum)
        for length in lengths:
            pos = int((length - len_min) / Y_gap)
            pos = min(pos, 27)
            yvalues[pos] = yvalues[pos] +1
        return X_names, yvalues, len_min, len_max

    def plotpixel(self):
        #self.sizeAnalysis('pixel')
        for class_name in self.classs_pixel:
            X_names, yvalues, xmin, xmax = self.generateplotX_Y(class_name, 'pixel')
            outname = os.path.join(r'E:\bod-dataset\analysis', class_name + '.jpg')
            self.plotbar_size(X_names, yvalues, class_name, xmin, xmax, fname=outname, type='pixel')

    def plotpixel_subplot(self):
        fig, axes = plt.subplots(2, 4)
        count = 0
        for class_name in self.classs_pixel:
            if class_name in self.selectedname:
                x = int(count / 4)
                y = count % 4
                print('x:', x)
                print('y:', y)
                X_names, yvalues, xmin, xmax = self.generateplotX_Y(class_name, 'pixel')
                outname = os.path.join(r'E:\bod-dataset\analysis', class_name + '.jpg')
                self.plotbar_size_ax(axes[x, y], X_names, yvalues, class_name, xmin, xmax)

                count = count + 1
        plt.show()
    def plotphysic(self):
        #self.sizeAnalysis('physic')
        for class_name in self.classs_physic:
            X_names, yvalues, xmin, xmax = self.generateplotX_Y(class_name, 'physic')
            self.plotbar_size(X_names, yvalues, class_name, xmin, xmax, 'physic')
if __name__ == '__main__':
    sizeplot = SizeDistribution(r'E:\bod-dataset')
    #sizeplot.plotphysic()
    #sizeplot.plotpixel()
    sizeplot.plotpixel_subplot()
    #X_names, yvalues, len_min, len_max = sizeplot.generateplotX_Y('small-vehicle', 'physic')
    #names = sizeplot.bugnames
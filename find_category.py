import os
import utils as util
import pickle
from utils import classname_15 as classname
from utils import datamap_15 as datamap
import random
import shutil
import codecs
from utils import wordname_15
import operations as operate

# def generatepickle(
#         basepath,
#         label
#         ):
#
#     initdic()
#     picklepath = os.path.join(basepath, 'pickle')
#     labelpath = os.path.join(basepath, label)
#     filelist = util.GetFileFromThisRootDir(labelpath)
#     for fullname in filelist:
#         name = util.mybasename(fullname)
#         objects = util.parse_bod_poly(fullname)
#         for obj in objects:
#             #wordname = datamap[obj['name']]
#             wordname = obj['name']
#             if name not in classedict[wordname]:
#                 classedict[wordname].append(name)
#     pickledir = os.path.join(picklepath, 'category-file.pickle')
#     with open(pickledir, 'wb') as f:
#         pickle.dump(classedict, f, pickle.HIGHEST_PROTOCOL)

def getcategory(
        basepath,
        label,
        ):
    classedict = {}
    def initdic():
        for clsname in classname:
            wordname = datamap[clsname]
            classedict[wordname] = []
    initdic()
    picklepath = os.path.join(basepath, 'pickle')
    pickledir = os.path.join(picklepath, 'category-file.pickle')
    if not os.path.isfile(pickledir):
        labelpath = os.path.join(basepath, label)
        filelist = util.GetFileFromThisRootDir(labelpath)
        for fullname in filelist:
            name = util.mybasename(fullname)
            objects = util.parse_bod_poly(fullname)
            for obj in objects:
                #wordname = datamap[obj['name']]
                wordname = obj['name']
                if name not in classedict[wordname]:
                    classedict[wordname].append(name)

        with open(pickledir, 'wb') as f:
            pickle.dump(classedict, f, pickle.HIGHEST_PROTOCOL)
    else:
        with open(pickledir, 'rb') as f:
            classedict = pickle.load(f)
    return classedict

def testgeneratepickle():
    basepath = r'E:\bod-dataset'
    label = r'wordlabel'
    classdict = getcategory(basepath,
                   label)
    print(classdict['baseketball-court'])

class findcategory():

    def __init__(self, basepath):
        self.basepath = basepath
        self.imgpath = os.path.join(basepath, 'images')
        self.labelpath = os.path.join(basepath, 'labelTxt')
        self.categorypath = os.path.join(basepath, 'categoryfind')
    def getCatIds(self, catNmes):
        imgIds = []
        picklepath = r'E:\bod-dataset\pickle\category-file.pickle'
        with open(picklepath, 'rb') as f:
            namedict = pickle.load(f)
            for name in catNmes:
                namefilelist = namedict[name]
                random.shuffle(namefilelist)
                imgIds.append(namefilelist[0])
        return imgIds

    def display(self, imgIds, catNmes):
        for index, imgname in enumerate(imgIds):

            srcimg = os.path.join(self.imgpath, imgname + '.png')
            dstimg = os.path.join(self.categorypath, 'images', imgname + '.png')
            shutil.copyfile(srcimg, dstimg)
            srctxt = os.path.join(self.labelpath, imgname + '.txt')
            objects = util.parse_bod_poly2(srctxt)
            dsttxt = os.path.join(self.categorypath, 'labelTxt', imgname + '.txt')
            with codecs.open(dsttxt, 'w', 'utf_16') as f_out:
                for obj in objects:
                    if datamap[obj['name']] == catNmes[index]:
                        outline = ' '.join(map(str, obj['poly'])) + ' ' + obj['name'] + ' ' + str(obj['difficult'])
                        f_out.write(outline + '\n')


    def test(self):
        catNmes = ['baseketball-court']
        #imgids = self.getCatIds(catNmes)
        imgids = self.getCatIds(catNmes)
        #imgids = self.getCatIds(wordname_15)
        self.display(imgids, catNmes)
def getallbasket():
    basepath = r'E:\bod-dataset'
    label = r'wordlabel'
    classdict = getcategory(basepath,
                   label)
    print(classdict['baseketball-court'])
    names = classdict['baseketball-court']
    operate.filecopy(r'E:\bod-dataset\images',
                     r'E:\bod-dataset\categoryfind\images',
                     names,
                     '.png')
    operate.filecopy(r'E:\bod-dataset\labelTxt',
                     r'E:\bod-dataset\categoryfind\labelTxt',
                     names,
                     '.txt')
if __name__ == '__main__':
    #testgeneratepickle()
    getallbasket()
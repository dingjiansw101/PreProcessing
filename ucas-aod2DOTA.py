import os
import utils as util
import codecs
import re



def parse_ucas_aod(filename, category):
    objects = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        splitlines = [x.strip().split('\t') for x in lines]

        for splitline in splitlines:
            coord = list(map(float, splitline))
            x, y, w, h = coord[9], coord[10], coord[11], coord[12]
            xmin, ymin = x, y
            xmax, ymax = x + w, y + h
            poly = [xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]
            object_struct = {}
            object_struct['poly'] = poly
            objects.append(object_struct)
    return objects
def aod2bod(srcpath, dstpath, category):
    filelist = util.GetFileFromThisRootDir(srcpath, '.txt')
    for fullname in filelist:

        objects = parse_ucas_aod(fullname, category)
        dstimgdir = ''
        imgname = util.mybasename(fullname)
        if (category == 'plane'):
            num = int(re.findall(r'\d+', imgname)[0])
            newnum = str(num + 510)
            dstimgname = 'P' + newnum.zfill(4)
            dstimgdir = os.path.join(dstpath, dstimgname + '.txt')
        else:
            dstimgdir = os.path.join(dstpath, imgname + '.txt')
        with codecs.open(dstimgdir, 'w', 'utf_16') as  f_out:
            for obj in objects:
                poly = obj['poly']
                outline = ' '.join(map(str, poly)) + ' ' + category
                f_out.write(outline + '\n')

def trans():
    aod2bod(r'E:\downloaddataset\CarPlane\bodformat\carannotation',
            r'E:\downloaddataset\CarPlane\bodformat\wordlabel',
            r'small-vehicle')
    aod2bod(r'E:\downloaddataset\CarPlane\bodformat\planeannotation',
            r'E:\downloaddataset\CarPlane\bodformat\wordlabel',
            r'plane')
def generateTrain():
    filelist = util.GetFileFromThisRootDir(r'E:\downloaddataset\CarPlane\bodformat\wordlabel')
    filenames = [util.mybasename(x) for x in filelist]
    #print('filenames: ', filenames)
    trainname = r'E:\downloaddataset\CarPlane\bodformat\train.txt'
    testname = r'E:\downloaddataset\CarPlane\bodformat\test.txt'
    testnames = ''
    with open(testname, 'r') as f_in:
        lines = f_in.readlines()
        testnames = [ util.mybasename(x.strip()) for x in lines]
    with open(trainname, 'w') as f_out:
        for name in filenames:
            if name not in testnames:
                f_out.write(name + '\n')

def testsplit():
    testname = r'E:\downloaddataset\CarPlane\bodformat\test.txt'
    testnames = ''
    with open(testname, 'r') as f_in:
        lines = f_in.readlines()
        testnames = [ util.mybasename(x.strip()) for x in lines]

    trainname = r'E:\downloaddataset\CarPlane\bodformat\train.txt'
    trainnames = ''
    with open(trainname, 'r') as f_in:
        lines = f_in.readlines()
        trainnames = [ util.mybasename(x.strip()) for x in lines]

    testset = set(testnames)
    trainset = set(trainnames)
    inter = testset.intersection(trainset)
    print('inter:', inter)
if __name__ == '__main__':
    testsplit()
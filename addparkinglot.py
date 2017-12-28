import os
import utils as util
import codecs
import shutil

rmnames = {
           '7B': 'half basketball', '12': 'electric pole', '13': 'parking lot', '15': 'lake',
           '17': 'airport', '18A': 'viaduct', '18B': '18B', '18C': '18C', '18D': '18D',
           '18E': '18E', '18F': '18F', '18G': '18G', '18H': '18H', '18I': '18I', '18J': '18J', '18K': '18K',
           '18L': '18L', '18M': '18M', '18N': '18N', '4A_area': '4A_area', '4B_area': '4B_area',
           '5A_area': '5A_area', '8_area': '8_area', '13_area': '13_area'
        }

## objects = {name1:[{poly:[], difficult:[]}, ...], name2:  }
def parse_gt(fullname):
    f = open(fullname, 'r', encoding='utf_16')
    lines = f.readlines()
    splitlines = [line.strip().split(' ') for line in lines]
    objects = {}
    for splitline in splitlines:
        if (len(splitline) < 9):
            continue
        clsname = splitline[8]
        if clsname not in objects:
            objects[clsname] = []
        object_struct = {}
        object_struct['poly'] = splitline[0:8]
        if len(splitline) <= 9:
            object_struct['difficult'] = '0'
        else:
            object_struct['difficult'] = splitline[9]
        objects[clsname].append(object_struct)
    return objects
class addparkinglot():
    def __init__(self):
        self.parkinglotpath1 = r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\parkinglotbackup\testparkinglot\labelTxt'
        self.parkinglotpath2 = r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\parkinglotbackup\trainparkinglot\labelTxt'
        self.filelist1 = util.GetFileFromThisRootDir(self.parkinglotpath1)
        self.filelist2 = util.GetFileFromThisRootDir(self.parkinglotpath2)
        self.namedict = {util.mybasename(x.strip()):x.strip() for x in (self.filelist1 + self.filelist2)}

    def getrmnameSet(self, objects):
        namelist = []
        for obj in objects:
            #if (obj['name'] in rmnames):
            namelist.append(obj['name'])
        nameSet = set(namelist)
        return nameSet

    def addparkinglot(self, srcpath, dstapath):
        needaddlist = util.GetFileFromThisRootDir(srcpath)
        for fullname in needaddlist:
            basename = util.mybasename(fullname)
            #with codecs.open(outname, 'w', 'utf_16'):
            srcobjects = parse_gt(fullname)
            addfullname = self.namedict[basename]
            addobjects = parse_gt(addfullname)

            dstname = os.path.join(dstapath, basename + '.txt')
            shutil.copyfile(fullname, dstname)

            srcnameset = {x for x in srcobjects}
            addnameset = {x for x in addobjects}

            diffnameset = addnameset.difference(srcnameset)
            with codecs.open(dstname, 'a', 'utf_16') as f_out:
                for clsname in diffnameset:
                    specificObjects = addobjects[clsname]
                    for obj in specificObjects:
                        poly = obj['poly']
                        outline = ' '.join(poly) + ' ' + clsname + ' ' + str(obj['difficult'])
                        print('outline: ', outline)
                        f_out.write(outline + '\n')

if __name__ == '__main__':
    addbase = addparkinglot()
    addbase.addparkinglot(
        r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\labelTxt',
        r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\addparkinglabelTxt\labelTxt'
    )
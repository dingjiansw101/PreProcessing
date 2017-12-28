import utils as util
from DatasetParser import parse_voc


## there may be something wrong
tiny_range, mid_range, large_range = range(10, 50), range(50, 300), range(300, 600)

## size
bod = {'tiny': 109004, 'mid': 77890, 'large': 2978, 'very_large': 831}
nwpu = {'tiny': 588, 'mid': 3230, 'large': 78, 'very_large': 0}
wilder = {'tiny': 130733, 'mid': 33700, 'large': 1954, 'very_large': 387}
vehicle_3k = {'tiny': 8743, 'mid': 708, 'large': 0, 'very_large': 0}
voc = {'tiny': 3585, 'mid': 16119, 'large': 6640, 'very_large': 0}
## percent
bod_percent = {'tiny': 0.5715903787564957, 'mid': 0.40843615464885186, 'large': 0.015615905360691757, 'very_large': 0.004357561233960661}
nwpu_percent = {'tiny': 0.15092402464065707, 'mid': 0.8290554414784395, 'large': 0.02002053388090349, 'very_large': 0.0}
vehicle_3k_percent = {'tiny': 0.9250872923500159, 'mid': 0.07491270764998413, 'large': 0.0, 'very_large': 0.0}
voc_percent = {'tiny': 0.13608411782569085, 'mid': 0.6118660795627088, 'large': 0.25204980261160037, 'very_large': 0.0}

def num2percent(sizedict):
    sum = 0
    outsizedict = {}
    for sizename in sizedict:
        sum = sum + sizedict[sizename]
    for sizename in sizedict:
        outsizedict[sizename] = sizedict[sizename] / sum
    return outsizedict
def getallbodobjects():
    filelist = util.GetFileFromThisRootDir(r'E:\downloaddataset\3K_VehicleDetection_dataset\Test_bod\labelTxt')
    allobjects = []
    for fullname in filelist:
        objects = util.parse_bod_rec(fullname)
        allobjects = allobjects + objects
    return allobjects

def getallvocobjects():
    filelist = util.GetFileFromThisRootDir(r'E:\downloaddataset\pascalvoc\VOCtrainval_11-May-2012\VOCdevkit\VOC2012\Annotations')
    allobjects = []
    for fullname in filelist:
        objects = parse_voc(fullname)
        allobjects = allobjects + objects
    return  allobjects
def wildercountonefile(filename):
    objects = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            line = line.strip()
            print('line: ', line)
            if '.jpg' in line:
                num = int(lines[index + 1].strip())
                picturelines = lines[(index + 2): (index + 2 + num)]
                for subline in picturelines:
                    object_struct = {}
                    ## add other information
                    splitline = subline.split(' ')
                    #object_struct['size'] = max(int(splitline[2]), int(splitline[3]))
                    object_struct['size'] = int(splitline[3])
                    objects.append(object_struct)
    return objects

def getallwiderobjects():
    valfile = r'E:\downloaddataset\wide_faces\wider_face_split\wider_face_split\wider_face_val_bbx_gt.txt'
    trainfile = r'E:\downloaddataset\wide_faces\wider_face_split\wider_face_split\wider_face_train_bbx_gt.txt'
    objects = wildercountonefile(valfile) + wildercountonefile(trainfile)
    return objects

def countrangenum(objects):
    range_dict = {'tiny': 0, 'mid': 0, 'large': 0, 'very_large': 0}
    for obj in objects:
        long_axis = obj['size']
        if long_axis in tiny_range:
            range_dict['tiny'] = range_dict['tiny'] + 1
        elif long_axis in mid_range:
            range_dict['mid'] = range_dict['mid'] + 1
        elif long_axis in large_range:
            range_dict['large'] = range_dict['large'] + 1
        elif long_axis >= 600:
            range_dict['very_large'] = range_dict['very_large'] + 1
    return range_dict
if __name__ == '__main__':
    #objects = getallbodobjects()
    # objects = getallwiderobjects()
    objects = getallvocobjects()
    range_dict = countrangenum(objects)
    print(range_dict)
    print(num2percent(range_dict))
    #print(num2percent(vehicle_3k))
    # print(num2percent(bod))
    # print(num2percent(nwpu))
    # print(num2percent(wilder))
import os
import utils as util
import numpy as np


nms_thresh = 0.4
## when get dets on several scale images, use the folowing function to do nms, then get the final predict
def py_cpu_nms(dets, thresh):
    """Pure Python NMS baseline."""
    print('dets:', dets)
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = dets[:, 4]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    ## index for dets
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= thresh)[0]
        order = order[inds + 1]

    return keep

def nmsbynamedict(nameboxdict, thresh):
    nameboxnmsdict = {x: [] for x in nameboxdict}
    for imgname in nameboxdict:
        print('imgname:', imgname)
        keep = py_cpu_nms(np.array(nameboxdict[imgname]), thresh)
        outdets = []
        for index in keep:
            outdets.append(nameboxdict[imgname][index])
        nameboxnmsdict[imgname] = outdets
    return nameboxnmsdict


def parse_comp4withnms(filename, thresh):
    nameboxdict = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        splitlines = [x.strip().split(' ') for x in lines]
        for splitline in splitlines:
            imgname = splitline[0]
            det = splitline[2:]
            det.append(splitline[1])
            det = list(map(float, det))
            if (imgname not in nameboxdict):
                nameboxdict[imgname] = []
            nameboxdict[imgname].append(det)
    nameboxnmsdict = nmsbynamedict(nameboxdict, thresh)
    return nameboxnmsdict
def NMScomp4():
    srcpath = r'E:\downloaddataset\CarPlane\results\bod-valid-car-480000-movejpg'
    dstpath = r'E:\downloaddataset\CarPlane\results\bod-valid-car-480000-nms'
    filelist = util.GetFileFromThisRootDir(srcpath)
    for fullname in filelist:
        print('fullname:', fullname)
        name = util.mybasename(fullname)
        dstname = os.path.join(dstpath, name + '.txt')
        nameboxdict = parse_comp4withnms(fullname, nms_thresh)
        print('nameboxdict: ', nameboxdict)
        with open(dstname, 'w') as f_out:
            for imgname in nameboxdict:
                for det in nameboxdict[imgname]:
                    print('det:', det)
                    confidence = det[-1]
                    bbox = det[0:-1]
                    outline = imgname + ' ' + str(confidence) + ' ' +  ' '.join(map(str, bbox))
                    #print('outline:', outline)
                    f_out.write(outline + '\n')
if __name__ == '__main__':
    NMScomp4()


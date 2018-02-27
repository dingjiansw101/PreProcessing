import os
import utils as util
import numpy as np
import codecs

def py_cpu_nms(dets, thresh):
    """Pure Python NMS baseline."""
    #print('dets:', dets)
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

def remove(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for filename in filelist:
        dstname = os.path.join(dstpath, util.mybasename(filename) + '.txt')
        with codecs.open(dstname, 'w', 'utf_16') as f_out:
            objects = util.parse_bod_poly(filename)
            bboxes = [list(util.dots4ToRec4(x['poly'])) for x in objects]
            for index, item in enumerate(bboxes):
                bboxes[index].append(1)
            bboxes = np.array(bboxes)
            print('filename:', filename)
            print('shape bboxes:', np.shape(bboxes))
            if (len(bboxes) == 0):
                continue
            keep = py_cpu_nms(bboxes, 0.99999)
            print('len bboxs:', len(bboxes))
            print('len keep:', len(keep))
            for id in keep:
                obj = objects[id]
                poly = obj['poly']
                poly = util.TuplePoly2Poly(poly)
                difficult = obj['difficult']
                category = obj['name']
                outline = ' '.join(map(str, poly)) + ' ' + category + ' ' + difficult
                f_out.write(outline + '\n')
if __name__ == '__main__':
    remove(r'I:\dota\wordlabel',
           r'I:\dota\wordlabelMS')
import os
import utils as util
import math
import numpy as np

size_thresh = 25

def distance(p1, p2):
    dist = np.sqrt(np.sum(p1 - p2)**2)
    print('dist:', dist)
    return dist

def max_len(poly):
    p1 = np.array([poly[0], poly[1]])
    p2 = np.array([poly[2], poly[3]])
    p3 = np.array([poly[4], poly[5]])
    p4 = np.array([poly[6], poly[7]])
    dis1 = distance(p1, p2)
    dist2 = distance(p2, p3)
    dist3 = distance(p3, p4)
    dist4 = distance(p4, p1)
    return max(dist4, max(dist3, max(dis1, dist2)))

def max_wh(poly):
    w = poly[2]
    h = poly[3]
    return max(w, h)

def rewrite(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for fullname in filelist:
        name = util.mybasename(fullname)
        with open(fullname, 'r') as f_in:
            dstname = os.path.join(dstpath, name + '.txt')
            with open(dstname, 'w') as f_out:
                lines = f_in.readlines()
                for line in lines:
                    splitline = line.strip().split(' ')
                    poly = list(map(float, splitline[2:]))
                    print('poly:', poly)
                    #long_axis = max_len(poly)
                    long_axis = max_wh(poly)
                    if (long_axis > size_thresh):
                        f_out.write(line)
if __name__ == '__main__':
    rewrite(r'E:\bod-dataset\results\bod_rfcn_1823781_nms',
            r'E:\bod-dataset\results\bod_rfcn_1823781_nms_filter_little')
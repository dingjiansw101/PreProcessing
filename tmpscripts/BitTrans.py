import os
import cv2
import utils as util
import numpy as np

def BitTrans(srcimg):
    dstimg = np.uint8(srcimg / 4)
    return dstimg

def TransBatch(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for filename in filelist:
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        basename = util.mybasename(filename)
        ext = os.path.splitext(filename)[1]
        dstname = os.path.join(dstpath, basename + ext)
        dstimg = BitTrans(img)
        # cv2.imshow('dstimg', dstimg)
        # cv2.waitKey()
        cv2.imwrite(dstname, dstimg)

TransBatch(r'I:\dota2\GF2\subset',
           r'I:\dota2\GF2\subset8')
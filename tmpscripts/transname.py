import os
import utils as util

def formattrans(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for filename in filelist:
        basename = util.mybasename(filename)
        outbasename = basename.replace(r'comp4_det_test_', r'Task1_')
        dstname = os.path.join(dstpath, outbasename + '.txt')
        with open(dstname, r'w') as f_out:
            with open(filename, r'r') as f:
                lines = f.readlines()
                #for i in range(10):
                for i in range(len(lines)):
                    outline = lines[i]
                    f_out.write(outline)

if __name__ == '__main__':
    formattrans(r'E:\bod-dataset\results\faster-rcnn-rot-59\nms0.1\com4_dota',
                r'E:\bod-dataset\results\faster-rcnn-rot-59\nms0.1\faster-rcnn-rot-59-Task1')
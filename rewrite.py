import os
import utils as util

def rewrite(srcpath, dstpath):
    with open(srcpath, 'r') as f:
        with open(dstpath, 'w') as f_out:
            lines = f.readlines()
            for line in lines:
                singleline = line.strip()
                outline = os.path.join(r'/home/dj/data/vehicle/JPEGImages', singleline + '.jpg')
                f_out.write(outline + '\n')
if __name__ == '__main__':
    rewrite(r'/home/dj/data/vehicle/trainname.txt',
            r'/home/dj/data/vehicle/train.txt')
    rewrite(r'/home/dj/data/vehicle/testname.txt',
            r'/home/dj/data/vehicle/test.txt')
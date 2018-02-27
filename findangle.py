import os
import utils as util
import numpy as np
import shutil

def calculateangle(poly):

    vec1 = np.array([float(poly[1][0]) - float(poly[0][0]), float(poly[1][1]) - float(poly[0][1]) ])
    vec2 = np.array([float(poly[2][0]) - float(poly[1][0]), float(poly[2][1]) - float(poly[1][1])])
    costheta = vec1.dot(vec2) / np.sqrt(np.sum(np.square(vec1)) + np.sum(np.square(vec2)))
    #return np.arccos(costheta)
    return costheta
def main():
    filelist = util.GetFileFromThisRootDir(r'I:\dota2\5du\checked\ship3\labelTxt')
    diffangles = {}
    # angle2name = {}
    for filename in filelist:
        objects = util.parse_bod_poly(filename)
        for obj in objects:
            poly = obj['poly']
            theta = calculateangle(poly)
            #diffangle = abs(theta - np.pi / 2)
            diffangle = abs(theta - 0)
            ## there may exist bug, for there may exist two same angle
            diffangles[diffangle] = filename
    results = sorted(diffangles.items(), key = lambda item:item[0])

    dstpath = r'I:\dota2\5du\checked\ship3\angle\images'
    srcimagepath = r'I:\dota2\5du\checked\ship3\images'
    for i in range(10):
        print(results[-i])
        filepath = results[-i][1]
        basename = util.mybasename(filepath)
        shutil.copyfile(filepath, os.path.join(dstpath, basename + '.txt'))
        shutil.copyfile(os.path.join(srcimagepath, basename + '.jpg'), os.path.join(dstpath, basename + '.jpg'))
if __name__ == '__main__':
    main()
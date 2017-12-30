import os
import utils as util
import xml.etree.ElementTree as ET
import cv2
import numpy as np

def getimagesize(imagename):
    img = cv2.imread(imagename)
    imagesize = np.shape(img)
    height = imagesize[0]
    width = imagesize[1]
    return height, width
def writelabelme(objects, imagename, dstname):
    annotation = ET.Element('annotation')
    filename = ET.Element('filename')
    filename.text = util.mybasename(imagename) + '.jpg'
    folder = ET.Element('folder')
    folder.text = r'part1'
    source = ET.Element('source')

    annotation.append(filename)
    annotation.append(folder)
    annotation.append(source)

    sourceImage = ET.Element('sourceImage')
    sourceImage.text = 'The MIT-CSAIL database of objects and scenes'
    sourceannotation = ET.Element('sourceAnnotation')
    sourceannotation.text = r'LabelMe Webtool'
    source.append(sourceImage)
    source.append(sourceannotation)

    id = 0
    for obj in objects:
        object = ET.Element('object')
        annotation.append(object)
        name = ET.Element('name')
        name.text = obj['name']
        deleted = ET.Element('deleted')
        deleted.text = str(0)
        vefified = ET.Element('verified')
        vefified.text = str(0)
        occluded = ET.Element('occluded')
        attributes = ET.Element('attributes')
        id = ET.Element('id')
        id.text = str(0)
        polygon = ET.Element('polygon')
        username = ET.Element('username')
        username.text = 'former'
        polygon.append(username)

        pt1 = ET.Element('pt')
        x1 = ET.Element('x')
        x1.text = str(obj['poly'][0])
        y1 = ET.Element('y')
        y1.text = str(obj['poly'][1])
        pt1.append(x1)
        pt1.append(y1)
        polygon.append(pt1)

        pt2 = ET.Element('pt')
        x2 = ET.Element('x')
        y2 = ET.Element('y')
        x2.text = str(obj['poly'][2])
        y2.text = str(obj['poly'][3])
        pt2.append(x2)
        pt2.append(y2)
        polygon.append(pt2)

        pt3 = ET.Element('pt')
        x3 = ET.Element('x')
        y3 = ET.Element('y')
        x3.text = str(obj['poly'][4])
        y3.text = str(obj['poly'][5])
        pt3.append(x3)
        pt3.append(y3)
        polygon.append(pt3)

        pt4 = ET.Element('pt')
        x4 = ET.Element('x')
        y4 = ET.Element('y')
        x4.text = str(obj['poly'][6])
        y4.text = str(obj['poly'][7])
        pt4.append(x4)
        pt4.append(y4)
        polygon.append(pt4)

        object.append(name)
        object.append(deleted)
        object.append(vefified)
        object.append(occluded)
        object.append(attributes)
        object.append(id)
        object.append(polygon)

    imagesize = ET.Element('imagesize')

    imagesize = getimagesize(imagename)
    nrows = ET.Element('nrows')
    nrows.text = imagesize[0]
    ncols = ET.Element('ncols')
    ncols.text = imagesize[1]

    tree = ET.ElementTree(annotation)
    print('tree:', tree)
    print('dstname:', dstname)
    tree.write(dstname)
def dota2labelme(srcpath, imagepath, dstpath):
    srclist = util.GetFileFromThisRootDir(srcpath)
    for filename in srclist:
        objects = util.parse_bod_poly2(filename)
        basename = util.mybasename(filename)
        dstname = os.path.join(dstpath, basename + '.xml')
        imagename = os.path.join(imagepath, basename + '.jpg')
        writelabelme(objects, imagename, dstname)

if __name__ == '__main__':
    dota2labelme(r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches\filtered\labelTxt',
                 r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches\filtered\images',
                 r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches\filtered\annotations')
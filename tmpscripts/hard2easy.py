import os
import utils as util
import codecs

def hard2easy(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for filename in filelist:
        basename = util.mybasename(filename)
        dstname = os.path.join(dstpath, basename + '.txt')
        objects = util.parse_bod_poly2(filename)
        with codecs.open(dstname, 'w', 'utf_16') as f_out:
            for obj in objects:
                poly = obj['poly']
                category = obj['name']
                difficult = obj['difficult']
                outline = ' '.join(map(str, poly)) + ' ' + category
                f_out.write(outline + '\n')
hard2easy(r'I:\dota2\5du\rotterdam1selectedsub\rotterdam1selectedsub\removerotterdamfirstbatch\hardlabel',
          r'I:\dota2\5du\rotterdam1selectedsub\rotterdam1selectedsub\removerotterdamfirstbatch\easylabel')
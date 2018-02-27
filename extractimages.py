import os
import shutil

def mybasename(fullname):
    return os.path.basename(os.path.splitext(fullname)[0])
def GetFileFromThisRootDir(dir,ext = None):
  allfiles = []
  needExtFilter = (ext != None)
  for root,dirs,files in os.walk(dir):
    for filespath in files:
      filepath = os.path.join(root, filespath)
      extension = os.path.splitext(filepath)[1][1:]
      if needExtFilter and extension in ext:
        allfiles.append(filepath)
      elif not needExtFilter:
        allfiles.append(filepath)
  return allfiles
def main():
    filelist = GetFileFromThisRootDir(r'labelTxt')
    names = [mybasename(x) for x in filelist]
    for img in names:
        srcfilename = os.path.join(r'images',img + '.jpg')
        if os.path.exists(srcfilename):
            shutil.copyfile(srcfilename, os.path.join(r'labeledimages', img + '.jpg'))
if __name__ == '__main__':
    main()

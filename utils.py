#-----------------------------------------
# some frequently used functions in data, and file process
# way of naming:
# for example, a full path name E:\code\Test\labelTxt2\1.txt, then
# basename indicates 1.txt, name indicates 1, suffix indicates .txt, path indicates E:\code\Test\labelTxt2, dir indicates E:\code\Test\labelTxt2\1.txt
# written by Jian Ding
#-----------------------------------------
## warp to calculate the set union, difference and intersection of files in two paths, not include the suffix, need to add by yourself
import os
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

def filesetcalc(path1, path2, calc = ''):
    if calc == '':
        print('please assigh a calc')
        return
    file1_list = GetFileFromThisRootDir(path1)
    file_set1 = {os.path.splitext(os.path.basename(x))[0] for x in GetFileFromThisRootDir(path1)}
    file_set2 = {os.path.splitext(os.path.basename(x))[0] for x in GetFileFromThisRootDir(path2)}
    inter_set = file_set1.intersection(file_set2)
    diff_set = file_set1.difference(file_set2)
    union_set = file_set1.union(file_set2)
    #suffix1 = os.path.splitext(os.path.basename(file1_list[0]))[1]
    if calc == 'u':
        print('union_set:', union_set)
        return union_set
    elif calc == 'd':
        print('diff_dict:', diff_set)
        return diff_set
    elif calc == 'i':
        print('inter_dict:', inter_set)
        return inter_set


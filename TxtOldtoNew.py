import os
import codecs,sys

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

list = GetFileFromThisRootDir('F:\documentation\毕业设计\workstation\标注规范\金璞\金璞-old', 'txt');
basedir = 'F:\documentation\毕业设计\workstation\标注规范\金璞\\';
print(basedir)

for txt in list:
    #f = open(txt, 'r', encoding='utf_16')
    f = open(txt, 'r')
    strlist = txt.split('\\');
    #print('yes', strlist[len(strlist) - 1])
    str = strlist[len(strlist) - 1];
    str = str[0:(len(str) - 8)];
    print('yes', str);
    dir = basedir + str + '.txt';
    out = codecs.open(dir, 'w', 'utf_16');

    cnt = 0;
    allcnt = 0;
    print(txt)
    flag = 0;
    label = -1;# -1 represtnt nothing
    str = '';
    while True:
        allcnt = allcnt + 1;
        print("allcnt", allcnt);
        cnt = cnt + 1;
        line = f.readline()
        if line:
            print(line)
            line = line.strip()
            if cnt < 5:
                out.write(line + ' ');
            elif cnt == 5:
                if (line == 'True'):
                    flag = 1;
            elif cnt == 6:
                cnt = 0;

                out.write(line + ' ');
                if flag == 1:
                    out.write('1');
                out.write('\n');
                flag = 0;# 0 represent flase

        else:
            break
    f.close()
print(object)
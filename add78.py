#coding:utf-8
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

list = GetFileFromThisRootDir('G:\Data\91Google\dingjian\Tool\change1', 'txt');
basedir = 'G:\Data\91Google\dingjian\Tool\change\\';
print(basedir)


for txt in list:
    print('txt', txt)
    f = open(txt, 'r', encoding='utf_16')
    #f = open(txt, 'r');
    strlist = txt.split('\\');
    #print('yes', strlist[len(strlist) - 1])
    str = strlist[len(strlist) - 1];
    str = str[0:(len(str) - 4)];
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
        line = f.readline();
        if line:
            print('line', line)
            line = line.strip()
            linelist = line.split(' ');
            print(linelist);
            if (len(linelist) == 9):
                if (linelist[len(linelist) - 1] == '5'):
                    linelist[len(linelist) - 1] = '4A';
                elif (linelist[len(linelist) - 1] == 'car'):
                    linelist[len(linelist) - 1] = '4A';
                elif (linelist[len(linelist) - 1] == '15'):
                    linelist[len(linelist) - 1] = '13';
               # elif (linelist[len(linelist) - 1] == '8'):
                #    print('In 8');
                 #   linelist[len(linelist) - 1] = '9';
            elif (len(linelist) == 10):
                print('In 10');
                if (linelist[len(linelist) - 1] == '0'):
                    print('change 0 to 1');
                    linelist[len(linelist) - 1] = '1';
                elif (linelist[len(linelist) - 2] == '5'):
                    linelist[len(linelist) - 2] = '4A';
                elif (linelist[len(linelist) - 1] == 'car'):
                    linelist[len(linelist) - 1] = '4A';
                elif (linelist[len(linelist) - 1] == '15'):
                    linelist[len(linelist) - 1] = '13';
                #elif (linelist[len(linelist) - 2] == '8'):
                 #   line[len(line)] = '9';
            outline = ''
            for item in linelist:
                outline = outline + item + ' ';
            print('outline', outline)
            out.write(outline + '\n');
        else:
            break;
    f.close()
print(object)
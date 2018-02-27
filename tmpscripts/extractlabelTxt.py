import os
import utils as util

def main():
    setfilename = r'I:\dota\trainset\trainset.txt'
    with open(setfilename, 'r') as f:
        lines = f.readlines()
        names = [x.strip() for x in lines]
    util.filecopy(r'I:\dota\dotalabelutf-8',
                  r'I:\dota\trainset\dotalabel',
                  names,
                  '.txt')
if __name__ == '__main__':
    main()
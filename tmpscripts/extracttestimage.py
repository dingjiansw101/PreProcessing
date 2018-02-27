import os
import utils as util

def main():
    setfilename = r'I:\dota\valset\valset.txt'
    with open(setfilename, 'r') as f:
        lines = f.readlines()
        names = [x.strip() for x in lines]
    util.filecopy(r'I:\dota\pngs',
                  r'I:\dota\valset\images',
                  names,
                  '.png')
if __name__ == '__main__':
    main()
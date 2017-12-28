import os
import utils as util
import pickle
import operations

def getduplicatenames():
    filename = r'E:\bod-dataset\pickle\duplicate.pkl'
    with open(filename, 'rb') as f_in:
        ## a list
        duplications = pickle.load(f_in)
    return duplications
def getmovelist():
    # srcpath = r'E:\bod-dataset'
    # srcimagepath = os.path.join(srcpath, 'images')
    # srclabelpath = os.path.join(srcpath, 'labelTxt')
    # outpath = r'E:\bod-dataset\duplicated_part'
    # outimagepath = os.path.join(outpath, 'images')
    # outlabelpath = os.path.join(outpath, 'labelTxt')
    duplications = getduplicatenames()
    print(duplications)
    movelist = []
    wordlabelpath = r'E:\bod-dataset\wordlabel'
    for duplicate_pair in duplications:
        image1name = duplicate_pair[0]
        image2name = duplicate_pair[1]
        fullname1 = os.path.join(wordlabelpath, image1name + '.txt')
        fullname2 = os.path.join(wordlabelpath, image2name + '.txt')
        objects1 = util.parse_bod_poly(fullname1)
        objects2 = util.parse_bod_poly(fullname2)
        if ( len(objects1) < len(objects2)):
            movelist.append(image1name)
        else:
            movelist.append(image2name)
    return movelist

def main():
    movelist = getmovelist()
    print('movelist:', movelist)
    print('len movelist:', len(movelist))
    operations.filemove(r'E:\bod-dataset\images',
                  r'E:\bod-dataset\duplicated_part\images',
                  movelist,
                  '.png')
    operations.filemove(r'E:\bod-dataset\labelTxt',
                  r'E:\bod-dataset\duplicated_part\labelTxt',
                  movelist,
                  '.txt')
if __name__ == '__main__':
    main()
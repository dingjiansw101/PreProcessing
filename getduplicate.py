import utils as util
import pickle

def duplicateread():
    path = r'E:\bod-dataset\pickle\duplicate.pkl'
    with open(path, 'rb') as f_in:
        img_pairs = pickle.load(f_in)
    return img_pairs

## choose less annotation to move
def find_less_annotation(img_pairx):
    for img_pair in img_pairs:
        img1 = img_pair[0]
        img2 = img_pair[1]


if __name__ == '__main__':
    img_pairs = duplicateread()
    print(img_pairs)

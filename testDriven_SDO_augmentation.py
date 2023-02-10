import unittest
import numpy as np
import pickle
import matplotlib.pyplot as plt

DATA_DIR = '/home/schatterjee/Documents/projects/HITS/data/euv/tiles/'
FILE_NAME = 'tile_20230206_000634_1024_0171_0320_0768.p'

def read_image(image_loc):
    image = pickle.load(open(image_loc, 'rb'))
    return image

def brighten_image(image,brightness=1):
    image = image.astype(float)/255
    image_out = image**brightness
    return image_out

def check_brightness(image,range=[0.5,1,2]):
    for i,b in enumerate(range):
        plt.subplot(1,len(range),i+1)
        im = brighten_image(image, brightness=b)
        plt.imshow(im)
    plt.show()

### json file with a list of aug: object like structure -> image, : List of aougment preformed, and their description
### 

image = read_image(DATA_DIR + FILE_NAME)
check_brightness(image, range=[0.5,1,2])

class Tests_on_Augmentations(unittest.TestCase):
    def test_XYZ(self):
        self.assertEqual(True,True)

    def test_dim(self):
        image = read_image(DATA_DIR + FILE_NAME)
        self.assertEqual(len(image.shape), 2)

    def test_resolution(self):
        image = read_image(DATA_DIR + FILE_NAME)
        self.assertEqual(image.shape, (64, 64))

    def test_range(self):
        image = read_image(DATA_DIR+FILE_NAME)
        image = brighten_image(image,brightness=2)
        diff = np.max(image) - np.min(image)
        self.assertNotEqual(diff,0)

if __name__=='__main__':
    unittest.main()
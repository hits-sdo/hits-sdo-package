'''
Team objective:
1. Create a list of augmentation functions for training data

Important details on the project:
1. The model takes in a fixed size image and outputs a vector representation of the image
2. The model uses the vector representation to return similar images

Where we left off:
1. Coordinates are wrong when grabbing adjacent tiles
2. change the equation for the coordinates
'''

import os
import unittest
import numpy as np
import pickle
import matplotlib.pyplot as plt
import cv2 as cv

DATA_DIR = '/home/schatterjee/Documents/projects/HITS/data/euv/tiles/'
FILE_NAME = 'tile_20230206_000634_1024_0171_0320_0768.p'
l = len("tile_20230206_000634_1024_0171_")

EXISTING_FILES = []

for root, dir, files in os.walk(DATA_DIR):
    for file in files:
        EXISTING_FILES.append(file)

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


# https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html
def translate_image( image, distanceX, distanceY):
    rows,cols = image.shape
    M = np.float32([[1, 0, distanceX], [0, 1, distanceY]])
    image = cv.warpAffine(image,M,(cols,rows))
    # image = crop(image, cols, cols+distanceY, rows, rows+distanceX)
    # image = resize(image, 64, 64)
    return image
    # Suggestion: 
    # img = cv2.imread("lenna.png")
    # crop_img = img[y:y+h, x:x+w] # <- y, x are range of rows.h, w are range of cols. New cropped img is stored

#example: 'tile_20230206_000634_1024_0171_0320_0768.p'
# 0320 is the x coordinate and 0768 is the y coordinate
# we need to grab all adjacent tiles and combine them into one image
def adj_imgs(file_name, ):
    l = len("tile_20230206_000634_1024_0171_")
    iStart = int(file_name[l:l+4])
    jStart = int(file_name[l+5:l+9])
    coordinates = [(0, 0), (1, 0), (2, 0), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    file_list = []
    
    for i,j in coordinates:
        i_s = iStart - 64 + i * 64
        j_s = jStart - 64 + j * 64

        tile_name = f"{file_name[0:l]}{str(i_s).zfill(4)}_{str(j_s).zfill(4)}.p"
        file_list.append(tile_name)

    return file_list 

for name in adj_imgs(FILE_NAME):
    print(f"{name}")
    
#dim = (width, height)
#resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def crop(image, x1, x2, y1, y2):
    return image[x1:x2, y1:y2]

def resize(image, width, height):
    dim = (width, height)
    return cv.resize(image, dim, interpolation = cv.INTER_AREA)
    

def check_translation(image,range=[(0,0)]):
    for i,t in enumerate(range):
        plt.subplot(1,len(range),i+1)
        im = translate_image(image, t[0], t[1])
        plt.imshow(im)
    plt.show()


### json file with a list of aug: object like structure -> image, : List of aougment preformed, and their description
### 

image = read_image(DATA_DIR + FILE_NAME)
#check_brightness(image, range=[0.5,1,2])
check_translation(image, range=[(0, 0), (-10, 0), (10, -20)])

# Remove the black void:
# 1. Find dimensions to zoom in to
# 2. Call Zoom in function
# 3. Scale back to 64x64


class Tests_on_Augmentations(unittest.TestCase):
    def test_XYZ(self):
        self.assertEqual(True,True)

    def test_dim(self):
        image = read_image(DATA_DIR + FILE_NAME)
        self.assertEqual(len(image.shape), 2)

    def test_resolution(self):
        image = read_image(DATA_DIR + FILE_NAME)
        image_tr = translate_image(image, 15, 15)
        self.assertEqual(image.shape, (64, 64))
        self.assertEqual(image_tr.shape, (64, 64))

    def test_range(self):
        image = read_image(DATA_DIR+FILE_NAME)
        image = brighten_image(image,brightness=2)
        self.assertNotEqual(np.max(image), np.min(image))
    
    def test_tile_start(self):
        self.assertEqual(int(FILE_NAME[l:l+4]),320)

    def test_adjacent_valid(self):
        f = adj_imgs(FILE_NAME)
        for i in f:
            self.assertEqual(i in EXISTING_FILES, True)
                
if __name__=='__main__':
    unittest.main()

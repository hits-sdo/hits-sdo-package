'''
Team objective:
1. Create a list of augmentation functions for training data
2. Apply a set of augmentations selected in random order or by the user

Important details on the project:
1. The model takes in a fixed size image and outputs a vector representation of the image
2. The model uses the vector representation to return similar images

Plan for Mar 10:
1. Perform a combination of augmentations depicted by a target dictionary
2. Work on the documentation of the code
'''

import os
import unittest
import numpy as np
import pickle
import matplotlib.pyplot as plt
import cv2 as cv
import glob
import streamlit as st
from PIL import Image
from augmentation_list import AugmentationList
from augmentation import Augmentations

"""glob.glob('/home/geeks/Desktop/gfg/data.txt')"""

# DATA_DIR = '/home/schatterjee/Documents/projects/HITS/data/mag/tiles/'
# FILE_LIST = glob.glob(DATA_DIR+"*.p")
# # FILE_NAME = 'tile_20230206_000000_1024_HMIB_0320_0768.p'
# FILE_NAME = FILE_LIST[0][-42:]
# l = len("tile_20230206_000634_1024_0171_")

DATA_DIR = './data/euv/tiles/'
FILE_NAME = 'tile_20230206_000000_1024_HMIB_0320_0768.p'
l = len("tile_20230206_000634_1024_0171_")

EXISTING_FILES = []

for root, dir, files in os.walk(DATA_DIR):
    for file in files:
        if file.endswith(".p"):
            EXISTING_FILES.append(file)


#image_loc = filepath
def read_image(image_loc, image_format):
    # := : assign and return the variable
    
    if(image_format == 'p'):
        image = pickle.load(imfile := open(image_loc, 'rb'))
        imfile.close()
        image = image.astype(float)/255
        return image
    if(image_format == 'jpg' or image_format == 'png' or image_format == 'jpeg'):
        im = Image.open(image_loc)
        image = np.array(im).astype(float)/255
        return image[:,:,0]


    #dim = (width, height)
    #resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

 #example: 'tile_20230206_000634_1024_0171_0320_0768.p'
    # 0320 is the x coordinate and 0768 is the y coordinate
    # we need to grab all adjacent tiles and combine them into one image
def stitch_adj_imgs(data_dir, file_name):
    l = len("tile_20230206_000634_1024_0171_")

    iStart = int(file_name[-11:-7])
    jStart = int(file_name[-6:-2])
    # coordinates of surrounding tiles
    coordinates = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    
    image_len = read_image(data_dir + file_name).shape[0]
    
    superImage = np.zeros((3*image_len, 3*image_len))
    for i,j in coordinates:
        i_s = iStart - image_len + i * image_len
        j_s = jStart - image_len + j * image_len

        #print(f'{i_s + image_len}{j_s + image_len}')

        tile_name = f"{file_name[0:l]}{str(i_s).zfill(4)}_{str(j_s).zfill(4)}.p"

        if tile_name in EXISTING_FILES:
            im = read_image(data_dir + tile_name)
            superImage[i*image_len: (i+1)*image_len, j*image_len: (j+1)*image_len] = im

    return superImage 

### json file with a list of aug: object like structure -> image, : List of aougment preformed, and their description
### 



# Remove the black void:
# 1. Find dimensions to zoom in to
# 2. Call Zoom in function
# 3. Scale back to 64x64

class Tests_on_Augmentations(unittest.TestCase):
    def setUp(self):
        
        DATA_DIR = f'./data/euv/tiles/'
        #FILE_NAME = 'tile_20230206_000000_1024_HMIB_0320_0768.p'
        FILE_NAME = EXISTING_FILES[100]
        self.image = read_image(DATA_DIR + FILE_NAME)
        self.superimage = stitch_adj_imgs(DATA_DIR, FILE_NAME)
        # augment_list = {"brighten": 1.2, "translate": (10,-15), "zoom": 1.5, "rotate": 45, "h_flip": True, "v_flip": True, 'blur':(2,2), 'p_flip': True}
        self.augument_list = AugmentationList(instrument = 'euv')

        augment_list = self.augument_list.randomize()

        # augment_list = {
        #     "rotate": -25, "h_flip": True, "v_flip": True
        # }
        self.augmentations = Augmentations(self.superimage, augment_list)
        self.assertEqual(True,True)

    # def test_rotate(self):
    #     # 2/23/23 - We want to try 45 degrees and see what it does to the edges
    #     # for 2/24 meeting
    #     image_ro = self.augmentations.rotate(self.superimage, rotation := 45)    
    #     # plt.subplot(1,2,1)
    #     # plt.imshow(self.image, vmin = 0, vmax = 255)
    #     # plt.subplot(1,2,2)
    #     # plt.imshow(image_ro, vmin = 0, vmax = 255)
    #     # plt.subplot(1,2,1)
    #     # plt.imshow(self.superimage[self.image.shape[0]:2*self.image.shape[0],self.image.shape[0]:2*self.image.shape[0]], vmin = 0, vmax = 255)
    #     # plt.subplot(1,2,2)
    #     # plt.imshow(image_ro[self.image.shape[0]:2*self.image.shape[0],self.image.shape[0]:2*self.image.shape[0]], vmin = 0, vmax = 255)
    #     # plt.title(f'rotated image {rotation} deg')
    #     # plt.show()

    # def test_dim(self):
    #     self.assertEqual(len(self.image.shape), 2)

    # def test_resolution(self):
    #     image_tr = self.augmentations.translate(self.image)
    #     self.assertEqual(self.image.shape, (64, 64))
    #     self.assertEqual(image_tr.shape, (64, 64))
    #     # self.assertEqual(image_tr[self.image.shape[0]:2*self.image.shape[0],self.image.shape[0]:2*self.image.shape[0]].shape, (64, 64))

    # def test_range(self):
    #     image = self.augmentations.brighten(self.image)
    #     self.assertNotEqual(np.max(image), np.min(self.image))
    
    # def test_tile_start(self):
    #     self.assertEqual(int(FILE_NAME[l:l+4]),320)

    # def test_adjacent_valid(self):
    #     superImage = stitch_adj_imgs(DATA_DIR, FILE_NAME)
    #     # plt.subplot(1,2,1)
    #     # plt.imshow(self.image, vmin = 0, vmax = 255)
    #     # plt.subplot(1,2,2)
    #     # plt.imshow(superImage, vmin = 0, vmax = 255)
    #     # plt.show()
            
    # def test_flip(self):
    #     image_tr = self.augmentations.v_flip(self.image)
    #     # ensuring same size
    #     self.assertEqual(image_tr.shape, (64, 64))
    #     # self.assertEqual(image_tr[self.image.shape[0]:2*self.image.shape[0],self.image.shape[0]:2*self.image.shape[0]].shape, self.image.shape)

    #     # plt.subplot(1,2,1)
    #     # plt.imshow(self.image, vmin = 0, vmax = 255)
    #     # plt.subplot(1,2,2)
    #     # plt.imshow(image_tr[self.image.shape[0]:2*self.image.shape[0],self.image.shape[0]:2*self.image.shape[0]], vmin = 0, vmax = 255)
    #     # plt.title('Vertically flipped image')
    #     # plt.show()
    
    # def test_blur(self):
    #     image_tr = self.augmentations.blur(self.image)
    #     # ensuring same size
    #     self.assertEqual(image_tr.shape, (64, 64))
    #     # self.assertEqual(image_tr[self.image.shape[0]:2*self.image.shape[0],self.image.shape[0]:2*self.image.shape[0]].shape, self.image.shape)

    #     # plt.subplot(1,2,1)
    #     # plt.imshow(self.image, vmin = 0, vmax = 255)
    #     # plt.subplot(1,2,2)
    #     # plt.imshow(image_tr[self.image.shape[0]:2*self.image.shape[0],self.image.shape[0]:2*self.image.shape[0]], vmin = 0, vmax = 255)
    #     # plt.title('blurred image')
    #     # plt.show()

    # def test_pole_flip(self):
    #     # flip and ensure different image
    #     image_tr = self.augmentations.p_flip(self.image)
    #     # self.assertTrue(self.image.all() == self.image.all())
    #     # image_tr = image_tr[self.image.shape[0]:2*self.image.shape[0],self.image.shape[0]:2*self.image.shape[0]]
    #     # plt.subplot(1,3,1)
    #     # plt.imshow(self.image, vmin = 0, vmax = 255, cmap = "gray")
    #     # plt.subplot(1,3,2)
    #     # plt.imshow(image_tr, vmin = 0, vmax = 255, cmap = "gray")
    #     # plt.title('Polarity flipped image')
    #     # plt.subplot(1,3,3)
    #     # plt.plot(image_tr[30,:],label='transformed image')
    #     # plt.plot(self.image[30,:],label='original image')
    #     # plt.plot([0,63],[128,128],'-k')
    #     # plt.legend(frameon=False)
    #     # plt.show()

    # def test_zoom(self):
    #     image_tr = self.augmentations.zoom(self.image, zoom = 1)
    #     s = image_tr.shape
    #     s1 = self.image.shape
    #     y1 = s[0]//2 - s1[0]//2
    #     y2 = s[0]//2 + s1[0]//2
    #     x1 = s[1]//2 - s1[1]//2
    #     x2 = s[1]//2 + s1[1]//2
    #     image_tr = image_tr[y1:y2, x1:x2]
    #     # plt.subplot(1,2,1)
    #     # plt.imshow(self.image, vmin = 0, vmax = 255)
    #     # plt.subplot(1,2,2)
    #     # plt.imshow(image_tr, vmin = 0, vmax = 255)
    #     # plt.title('zoomed image')
    #     # plt.show()

    def test_augmentations(self):
        augmented_img, title = self.augmentations.perform_augmentations()
        
        plt.subplot(1,2,1)
        plt.imshow(self.image,cmap='gray',vmin=0,vmax=1)
        plt.subplot(1,2,2)
        plt.imshow(augmented_img,cmap='gray',vmin=0,vmax=1)
        plt.title(title)
        plt.show()

        self.assertNotEqual(np.max(augmented_img), np.min(self.image))


if __name__=='__main__':
    unittest.main()

    
    #image = read_image(DATA_DIR + FILE_NAME)
    #check_brightness(image, range=[0.5,1,2])
    #check_translation(image, range=[(0, 0), (-10, 0), (10, -20)])

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

import numpy as np
import cv2 as cv
import pickle
import os






class Augmentations():
    """
    The purpose of this class is to hold a dictionary of all different augmentations usable

    Parameters used: 
        image (uint8/float)
        self 
        dictionary of augmentations
            rotation    (float) : degrees
            brighten  (float) : 1 = no brighten transformation applied
            zoom        (float) : 1 = 1X zoom
            translate   (integer, integer) : (x,y) || (0,0)  = no translation 

    Combination of augmentations: 
    """

    # https://www.pythoncheatsheet.org/cheatsheet/dictionaries
    def __init__(self, image=None, dct={"brighten": 1, "translate": (0,0), "zoom": 1, "rotate": 0, "h_flip": False, "v_flip": False, 'blur':(1,1), "p_flip": False} ):
        self.image = image
        self.augmentations = dct
        #self.augmentationPointer = {"brighten": self.brighten, "translate": self.translate_image, "zoom": self.zoom, 
       #                        "blur": self.blur_image, "p_flip": self.pole_flip_image}
        # augmentation_name
        # augmentationPointer[augmentation_name](image, augmentations[augmentation_name])
        method_names = [attribute for attribute in dir(self) if callable(getattr(self, attribute)) and attribute.startswith('__') is False]
        self.augmentationPointer = {}

        for name in method_names:
            self.augmentationPointer[name] = getattr(self, name)

    def rotate(self, image, rotation=0):
        s = image.shape
        cy = (s[0]-1)/2
        cx = (s[1]-1)/2    #set the x, y vals of center of image
        # true center = 31.5
        M = cv.getRotationMatrix2D((cx,cy),rotation,1)
        return cv.warpAffine(image,M,(s[1],s[0]))
        
        
    def brighten(self, image, brighten=1):
        #image = image.astype(float)/255
        image_out = image**brighten
        return image_out
    

    # https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html
    def translate(self, image, translate=(0,0)):
        rows,cols = image.shape
        M = np.float32([[1, 0, translate[0]], [0, 1, translate[1]]])
        image = cv.warpAffine(image,M,(cols,rows))
        return image

    def zoom(self, image, zoom):
        dim = image.shape
        return cv.resize(image, (int(zoom*dim[0]), int(zoom*dim[1])), interpolation = cv.INTER_AREA)
        
    def v_flip(self, image, v_flip=True):
        if v_flip == True:
            image = cv.flip(image, 1) 
        return image
    
    def h_flip(self, image, h_flip=True):
        if h_flip == True:
            image = cv.flip(image, 0) 
        return image
    
    def blur(self, image, blur=(1,1)):
        image = cv.blur(image,(blur[0],blur[1]), 0)
        return image

    def p_flip(self, image, p_flip=True):
        if p_flip == True:
            image = 1 - image
        return image


    def perform_augmentations(self):
        #*args **kwargs   // pass var num of args to a function
        augmentations_list = list(self.augmentations.keys())

        augment_image = self.image
        title = 'original'
        for augmentation_name in augmentations_list:
            augment_image = self.augmentationPointer[augmentation_name](
                augment_image, self.augmentations[augmentation_name]
            )

            u_arrow = "\u27F6"
            title = title + u_arrow + augmentation_name

        s = augment_image.shape
        s1 = (64, 64)  #TODO make flexible
        y1 = s[0]//2 - s1[0]//2
        y2 = s[0]//2 + s1[0]//2
        x1 = s[1]//2 - s1[1]//2
        x2 = s[1]//2 + s1[1]//2
        augment_image = augment_image[y1:y2, x1:x2]

    
        return augment_image,title
        
 

### json file with a list of aug: object like structure -> image, : List of aougment preformed, and their description
### 



# Remove the black void:
# 1. Find dimensions to zoom in to
# 2. Call Zoom in function
# 3. Scale back to 64x64

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


class Augmentations():
    """
    The purpose of this class is to hold a dictionary of all different augmentations usable

    Parameters used: 
        image (uint8/float)
        self 
        dictionary of augmentations
            rotation    (float) : degrees
            brightness  (float) : 1 = no brightness transformation applied
            zoom        (float) : 1 = 1X zoom
            translate   (integer, integer) : (x,y) || (0,0)  = no translation 

    Combination of augmentations: 
    """

    # https://www.pythoncheatsheet.org/cheatsheet/dictionaries
    def __init__(self, image=None, dct={"brightness": 1, "translate": (0,0), "zoom": 1, "rotate": 0, "h_flip": False, "v_flip": False, 'blur':(1,1), "p_flip": False} ):
        self.image = image
        self.augmentations = dct

    def rotate_image(self, image, rotation=0):
        s = image.shape
        cy = (s[0]-1)/2
        cx = (s[1]-1)/2    #set the x, y vals of center of image
        # true center = 31.5
        M = cv.getRotationMatrix2D((cx,cy),rotation,1)
        return cv.warpAffine(image,M,(s[1],s[0]))
        
        
    def brighten_image(self, image, brightness=1):
        image = image.astype(float)/255
        image_out = image**brightness
        return image_out
    

    # https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html
    def translate_image(self, image, translate=(0,0)):
        rows,cols = image.shape
        M = np.float32([[1, 0, translate[0]], [0, 1, translate[1]]])
        image = cv.warpAffine(image,M,(cols,rows))
        return image

    def resize(self, image, zoom):
        dim = image.shape
        return cv.resize(image, (int(zoom*dim[0]), int(zoom*dim[1])), interpolation = cv.INTER_AREA)
        
    def v_flip_image(self, image, v_flip=True):
        if v_flip == True:
            image = cv.flip(image, 1) 
        return image
    
    def h_flip_image(self, image, h_flip=True):
        if h_flip == True:
            image = cv.flip(image, 0) 
        return image
    
    def blur_image(self, image, blur=(1,1)):
        image = cv.blur(image,(blur[0],blur[1]), 0)
        return image

    def pole_flip_image(self, image, p_flip=True):
        if p_flip == True:
            image = 255 - image
        return image


    def perform_augmentations(self):
        ...
        


### json file with a list of aug: object like structure -> image, : List of aougment preformed, and their description
### 



# Remove the black void:
# 1. Find dimensions to zoom in to
# 2. Call Zoom in function
# 3. Scale back to 64x64

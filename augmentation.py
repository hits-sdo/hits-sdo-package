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
    def __init__(self, image: float=None, dct: dict={"brighten": 1, "translate": (0,0), "zoom": 1, "rotate": 0, "h_flip": False, "v_flip": False, 'blur':(1,1), "p_flip": False} ):
        '''
        Initialize an object of the Augmentation class
        Parameters:
            image (float): 
                Optional parameter to pass in an image. Otherwise defaults to None.
            dct (dict):
                Optional parameter to specify a dictionary with the given augmentation parameters and values.
        Returns:
            dict(str, Any):
                randomized dictionary
        '''
        self.image = image
        self.augmentations = dct
        self.method_names = [attribute for attribute in dir(self) if callable(getattr(self, attribute)) and attribute.startswith('__') is False]
        self.method_names.remove('perform_augmentations')
        self.augmentationPointer = {}
        self.TARGET_SHAPE = (64,64)

        for name in self.method_names:
            self.augmentationPointer[name] = getattr(self, name)

    def rotate(self, image, rotation: float=0):
        '''
        Initialize an object of the Augmentation class
        Parameters:
            rotation (float):
                Optional parameter to specify a float for the number of degrees of rotation.
        Returns:
            dict(str, Any):
                randomized dictionary
        '''
        s = image.shape
        cy = (s[0]-1)/2 # y center : float
        cx = (s[1]-1)/2 # x center : float
        M = cv.getRotationMatrix2D((cx,cy),rotation,1) # rotation matrix 
        return cv.warpAffine(image,M,(s[1],s[0])) # Affine transformation to rotate the image and output size s[1],s[0]
        
        
    def brighten(self, image, brighten: float=1):
        image_out = image**brighten # use brighten parameter as an exponent to brighten/darken image
        return image_out
    

    # https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html
    def translate(self, image, translate: int=(0,0)):
        s = image.shape
        M = np.float32([[1, 0, translate[0]], [0, 1, translate[1]]]) # Translation Matrix
        image = cv.warpAffine(image,M,(s[1],s[0]))# Affine transformation to translate the image and output size s[1],s[0]
        return image

    def zoom(self, image, zoom : float=1):
        s = image.shape
        return cv.resize(image, (int(zoom*s[0]), int(zoom*s[1])), interpolation = cv.INTER_AREA) # Resize the image using zoom as scaling factor with area interpolation
        
    def v_flip(self, image):
        image = cv.flip(image, 0)  # vertically flip the image
        return image
    
    def h_flip(self, image):
        image = cv.flip(image, 1) # horizontally flip the image
        return image
    
    def blur(self, image, blur: int =(1,1)):
        image = cv.blur(image,(blur[0],blur[1]), 0) # Perform an average blurring with kernel size defined by blur
        return image

    def p_flip(self, image):
        image = 1 - image # flip the polarity of the image
        return image


    def perform_augmentations(self):
        '''
        general function to perform the sequence of augmentation 
        defined by the input dictionary in Augmentations class
        '''
        #*args **kwargs   // pass var num of args to a function
        augmentations_list = list(self.augmentations.keys()) # the input dictionary defining the augmentation sequence

        augment_image = self.image
        title = 'original' # initialize the augmented image title showing sequence of augmentations
        for augmentation_name in augmentations_list:
            if type(self.augmentations[augmentation_name]) == bool:
                augment_image = self.augmentationPointer[augmentation_name](
                    augment_image
                ) # for loop for updating the image through sequence of augmentations
            else:
                augment_image = self.augmentationPointer[augmentation_name](
                    augment_image, self.augmentations[augmentation_name]
                ) # for loop for updating the image through sequence of augmentations

            u_arrow = "\u27F6" # unicode character for right-ward arrow
            title = title + u_arrow + augmentation_name # updating the title through sequence of augmentations

        s = augment_image.shape #shape of the augmented image
        s1 = self.TARGET_SHAPE  
        y1 = s[0]//2 - s1[0]//2
        y2 = s[0]//2 + s1[0]//2
        x1 = s[1]//2 - s1[1]//2
        x2 = s[1]//2 + s1[1]//2
        augment_image = augment_image[y1:y2, x1:x2] # central part of the augmented image of size TARGET_SHAPE

    
        return augment_image,title
        
    
 

### json file with a list of aug: object like structure -> image, : List of aougment preformed, and their description
### 



# Remove the black void:
# 1. Find dimensions to zoom in to
# 2. Call Zoom in function
# 3. Scale back to 64x64

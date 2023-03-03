'''
Team objective:
1. Create a list of augmentation functions for training data

Important details on the project:
1. The model takes in a fixed size image and outputs a vector representation of the image
2. The model uses the vector representation to return similar images

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
    def __init__(self, image, dct={"brightness": 1, "translate": (0,0), "zoom": 1, "rotate": 0, "h_flip": False, "v_flip": False, 'blur':(1,1)}):
        self.image = image
        self.zoom = dct["zoom"]
        self.brightness = dct["brightness"]
        self.translate = dct["translate"] # pixels to translate the image by
        self.rotation = dct["rotate"] # degrees to rotate the image by
        self.h_flip = dct["h_flip"]
        self.v_flip = dct["v_flip"] 
        self.blur = dct['blur'] # level of blur we want on the image (increase values for more blur)
        """"""

    def rotate_image(self):
        s = self.image.shape
        cy = (s[0]-1)/2
        cx = (s[1]-1)/2    #set the x, y vals of center of image
        # true center = 31.5
        M = cv.getRotationMatrix2D((cx,cy),self.rotation,1)
        return cv.warpAffine(self.image,M,(s[1],s[0]))
        
        
    def brighten_image(self):
        image = self.image.astype(float)/255
        image_out = image**self.brightness
        return image_out
    

    # https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html
    def translate_image(self):
        rows,cols = self.image.shape
        M = np.float32([[1, 0, self.translate[0]], [0, 1, self.translate[1]]])
        image = cv.warpAffine(self.image,M,(cols,rows))
        # image = crop(image, cols, cols+distanceY, rows, rows+distanceX)
        # image = resize(image, 64, 64)
        return image

    def resize(self):
        dim = self.image.shape
        return cv.resize(self.image, (self.zoom*dim[0],self.zoom*dim[1]), interpolation = cv.INTER_AREA)
        
    def h_flip_image(self):
        image = self.image
        if self.v_flip == True:
            image = cv.flip(image, 1) 
        return image
    
    def v_flip_image(self):
        image = self.image
        if self.h_flip == True:
            image = cv.flip(image, 0) 
        return image
    
    def blur_image(self):
        image = cv.blur(self.image,(self.blur[0],self.blur[1]), 0)
        return image
       # image = cv2.blur(image, ksize) 
       # # ksize
        #ksize = (30, 30)
        # Syntax: cv2.blur(src, ksize[, dst[, anchor[, borderType]]])

"""
# Average Blurring -> can do even kernel values
image = cv2.blur(image, (10, 10))

# Gaussian Blurring -> can only take odd kernal values
# Again, you can change the kernel size
gausBlur = cv2.GaussianBlur(img, (5,5),0) 
cv2.imshow('Gaussian Blurring', gausBlur)
cv2.waitKey(0)
  
# Median blurring
medBlur = cv2.medianBlur(img,5)
cv2.imshow('Media Blurring', medBlur)
cv2.waitKey(0)
  
# Bilateral Filtering
bilFilter = cv2.bilateralFilter(img,9,75,75)
cv2.imshow('Bilateral Filtering', bilFilter)
cv2.waitKey(0)
cv2.destroyAllWindows()"""


### json file with a list of aug: object like structure -> image, : List of aougment preformed, and their description
### 



# Remove the black void:
# 1. Find dimensions to zoom in to
# 2. Call Zoom in function
# 3. Scale back to 64x64

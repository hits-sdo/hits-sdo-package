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

import numpy as np
import cv2 as cv


class Augmentations():
    # https://www.pythoncheatsheet.org/cheatsheet/dictionaries
    def __init__(self, image, dct={"brightness": 1, "translate": (0,0), "zoom": 1, "rotate": 0}):
        self.image = image
        self.zoom = dct["zoom"]
        self.brightness = dct["brightness"]
        self.translate = dct["translate"] # pixels to translate the image by
        self.rotation = dct["rotate"] # degrees to rotate the image by
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
        


### json file with a list of aug: object like structure -> image, : List of aougment preformed, and their description
### 



# Remove the black void:
# 1. Find dimensions to zoom in to
# 2. Call Zoom in function
# 3. Scale back to 64x64

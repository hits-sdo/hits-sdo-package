'''
Objective:
'
GUI features:
+ Button -> Option to upload custom file
    - later on implement uploading multiple files
    - simultaneous processing/rendering of image augmentation data (hard limit to # of images processed at once)
    - option to specify output folder for batch of augmentation
    - (json file for # order and list of augmentations performed on image(s))
    - hard cap on user data stored in the cloud 
    - user selects path/folder
    - display loading % to user
    - drag and drop component - specify order & add/remove augmentations. Augmentation name and details are shown in box. Click on box to expand/specify values
    - download button (images and meta data)

+ Display -> Display sample visualization of data to user

+ Menu -> Settings sidebar
    - Specify default file path (default file format)
    - History of past uploads (text file, size data, augmentations performed, image format)
    - (App cannot access local file folder, MUST be cloud storage)
    - choose set of augmentations on dataset
    - select/de-select all
    - Sort based on meta data
    - search is a certain set of augmentations is performed on a certain set of images

+ Misc/User
    - login
    - saving presets of augmentations
    - 

Plan for today Mar 30, 2023:
- [] Add file upload option
- [] render uploaded image
- [] sidebar placeholder
- [] perform random augmentations

Plan for Mar 31st 2023:
- [] Get rid of dark img problem
- [] Add download button to download augmented image & augmentation sequence
- [] 

Plan for Apr 6th 2023:
- [] Get rid of dark image rendering bug
- [] Downloading a JSON file from our program to local computer of image augmentation state
- [] Upload a JSON file and perform the augmentation defined in that

Plan for Apr 7th 2023:
- [] Sidebar to randomize augmentation
- [] Make randomizer outcome editable for user-defined dictionary 
- [] Add image info in the dictionary
'''

# https://docs.streamlit.io/library/api-reference/widgets/st.multiselect
# https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader
# > suggested syntax: uploaded_file = st.file_uploader("Choose an image...", type="jpg")



import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
import cv2 as cv
import glob
from augmentation_list import AugmentationList
from augmentation import Augmentations
import streamlit as st
from PIL import Image
from augmentation_test import read_image
from io import BytesIO
import tempfile
import json

def button_augmentation_randomize(img, col2, aug_dict = None):
    # Place JSON into augment_dict
    augment_list = AugmentationList(instrument = 'euv')
    if aug_dict is None:
        augment_dict = augment_list.randomize()
    else:
        augment_dict = aug_dict
    augments = Augmentations(img, augment_dict)
    augmented_img, title = augments.perform_augmentations()
    col2.header(title)
    col2.image(augmented_img,use_column_width='always',clamp=True)
    js = json.dumps(augment_dict)   # Convert transformation dictionary to JSON string
    augmented_img *= 255  # un-normalize image
    a_img = pickle.dumps(augmented_img) # serialize into bytestring
    col2.download_button(label="Download Augmented Image", data=a_img, file_name="augmented_img.p", mime="image/p")
    col2.download_button(label="Download Augmentation Dictionary", data=js, file_name="augmented_dict.json", mime="application/json")
    #st.write(st.session_state['dict'])


def main():
    st.header("Image Augmentation Tool")
    uploaded_file = st.file_uploader("Choose an image...", type=["p", "jpg"],key='img')
    uploaded_dict = st.file_uploader("Choose a dictionary", type=["json"])
    col1, col2 = st.columns([1,1])
    if uploaded_file is not None:
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # write to temp file
            temp_file.write(uploaded_file.read())
            #get path
            file_path = temp_file.name
            img = read_image(file_path, uploaded_file.name.split('.')[-1])
            col1.header("Original Image")
            col1.image(img,use_column_width='always',clamp=True)
            aug_dict = None
            if uploaded_dict and submitted is not None:
                aug_dict = json.load(uploaded_dict)
        
        col1.button("Apply random augmentation", on_click=button_augmentation_randomize,args=([img, col2, aug_dict]))
        


                
      


if __name__ == '__main__':
    main()






    
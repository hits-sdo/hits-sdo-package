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
- [] flixible target resolution
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


def main():

        



    st.header("Image Augmentation Tool")
    uploaded_file = st.file_uploader("Choose an image...", type=["p", "jpg"],key='img')
    uploaded_dict = st.file_uploader("Choose a dictionary", type=["json"])
    col1, col2 = st.columns([1,1])

    # Setup Sidebar
    st.sidebar.title("Settings") 
    imageInst = st.sidebar.selectbox("Select Instrument", ('euv', 'mag'))
    augment_list = AugmentationList(instrument = imageInst)
    if 'random_init_dict' not in st.session_state:
        st.session_state['random_init_dict'] = augment_list.randomize()
    
    
    #augment_dict = augment_list.randomize()

    options = st.sidebar.multiselect("Choose augmentations: ", augment_list.keys, default=list(st.session_state['random_init_dict'].keys()))
    #st.sidebar.write('You selected: ', options)
    user_dict = {}
    for key in options: 
        #TODO switch to python 3.10 and use match statement 
        if 'rotate' == key:
            rotation = st.sidebar.slider("Rotation:", -180.0, 180.0, st.session_state['random_init_dict'][key])
            user_dict['rotate'] = rotation    
        if 'v_flip' == key:
            user_dict['v_flip'] = True
        if 'h_flip' == key:
            user_dict['h_flip'] = True
        if 'blur' == key :
            user_dict['blur'] = (2,2)
        if 'brighten' == key:
            brighten = st.sidebar.slider("Brighten:", 0.5, 1.5, st.session_state['random_init_dict'][key])
            user_dict['brighten'] = brighten
        if 'zoom' == key:
            zoom = st.sidebar.slider("Zoom:", 0.5, 5.0, st.session_state['random_init_dict'][key])
            user_dict['zoom'] = zoom
        if 'translate' == key:
            x_translate = st.sidebar.slider("X-Axis Translation:", -10, 10, st.session_state['random_init_dict'][key][0])
            y_translate = st.sidebar.slider("Y-Axis Translation:", -10, 10, st.session_state['random_init_dict'][key][1])
            user_dict['translate'] = (x_translate, y_translate) 
          

    
    
    
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
            if uploaded_dict is not None:
                aug_dict = json.load(uploaded_dict)
                
            st.sidebar.button("Random augmentation", on_click=button_augmentation_randomize,args=([img, col2, aug_dict]))
            st.sidebar.button("Apply augmentation", on_click=button_augmentation_randomize,args=([img, col2, user_dict]))
            


                
      


if __name__ == '__main__':
    main()






    
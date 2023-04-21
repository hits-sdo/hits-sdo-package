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

Plan for April 20th 2023:
- [] User defined target resolution (default: 64x64)
- [] Allow user to specify target crop location (default: center)
    - Crops the input image to the specified region
    - Selecting a region by dragging a box
    - Be able to use superimage when cropping
- [] Allow user to work with RGB colors  
- [] Work with Pylint?

Left off: changing augments in the widget is finnicky
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
from streamlit_cropper import st_cropper
from streamlit_modal import Modal

def generate_augmentation():
    # del st.sesstion_state['random_init_dict']
    # Place JSON into augment_dict
    augment_list = AugmentationList(st.session_state['instrument'])
    st.session_state['random_init_dict'] = augment_list.randomize()

def apply_augmentation(img, col2, user_dict):
    st.session_state['random_init_dict'] = user_dict
    augments = Augmentations(img, st.session_state['random_init_dict'])
    augmented_img, title = augments.perform_augmentations()
    col2.header(title)
    col2.image(augmented_img,use_column_width='always',clamp=True)
    js = json.dumps(st.session_state['random_init_dict'])   # Convert transformation dictionary to JSON string
    augmented_img *= 255  # un-normalize image
    a_img = pickle.dumps(augmented_img) # serialize into bytestring
    col2.download_button(label="Download Augmented Image", data=a_img, file_name="augmented_img.p", mime="image/p")
    col2.download_button(label="Download Augmentation Dictionary", data=js, file_name="augmented_dict.json", mime="application/json")

def refresh():
    st.experimental_rerun()

    
def main():
    # uploaded_dict = st.empty()
    # st.caching.clear_cache()
    st.header("Image Augmentation Tool")
    uploaded_file = st.file_uploader("Choose an image...", type=["p", "jpg"],key='img')
    with st.form('my-form', clear_on_submit = True):
        uploaded_dict = st.file_uploader("Choose a dictionary", type=["json"])
        submitted = st.form_submit_button("UPLOAD!")
    
    # with st.form("my-form", clear_on_submit=True):
    #    file = st.file_uploader("FILE UPLOADER")
    col1, col2 = st.columns([1,1])
    cropContainer = col1.empty()

    # Setup Sidebar
    st.sidebar.title("Settings") 
    
    # Get Instument
    imageInst = st.sidebar.selectbox("Select Instrument", ('euv', 'mag'), key='instrument', on_change=generate_augmentation)
    augment_list = AugmentationList(instrument = imageInst)
    if 'random_init_dict' not in st.session_state:
        st.session_state['random_init_dict'] = augment_list.randomize()

    # Target Resolution

    
    # user_dict = None
    if uploaded_dict is not None and submitted is True:
        st.session_state["random_init_dict"] = json.load(uploaded_dict)
         # uploaded_dict = st.empty() #new 
    #augment_dict = augment_list.randomize()

    user_dict = {}
    options = st.sidebar.multiselect("Choose augmentations: ", augment_list.keys, default=list(st.session_state['random_init_dict'].keys()))#,on_change=refresh)
    #st.sidebar.write('You selected: ', options)
    
    
    for key in options: 
        #TODO switch to python 3.10 and use match statement 
        if 'rotate' == key:
            rotation = st.sidebar.slider("Rotation:", -180.0, 180.0, float(st.session_state['random_init_dict'][key]) if key in st.session_state['random_init_dict'] else 0.0 )
            
            user_dict['rotate'] = rotation    
        if 'v_flip' == key:
            user_dict['v_flip'] = True
        if 'h_flip' == key:
            user_dict['h_flip'] = True
        if 'blur' == key :
            user_dict['blur'] = (2,2)
        if 'brighten' == key:
            
            brighten = st.sidebar.slider("Brighten:", 0.5, 1.5, float(st.session_state['random_init_dict'][key]) if key in st.session_state['random_init_dict'] else 1.0 )
            user_dict['brighten'] = brighten

        if 'zoom' == key:
            zoom = st.sidebar.slider("Zoom:", 0.5, 5.0, float(st.session_state['random_init_dict'][key]) if key in st.session_state['random_init_dict'] else 1.0 )
            user_dict['zoom'] = zoom

        if 'translate' == key:
            x_translate = st.sidebar.slider("X-Axis Translation:", -10, 10, st.session_state['random_init_dict'][key][0] if key in st.session_state['random_init_dict'] else 0 )
            y_translate = st.sidebar.slider("Y-Axis Translation:", -10, 10, st.session_state['random_init_dict'][key][1] if key in st.session_state['random_init_dict'] else 0)
            user_dict['translate'] = (x_translate, y_translate)

    


    # if user_dict != st.session_state['random_init_dict']:
    #     st.session_state['random_init_dict'] = user_dict
    
    cropper_modal = Modal(key="Crop State", title="Crop Image")
    if uploaded_file is not None:
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # write to temp file
            temp_file.write(uploaded_file.read())
            #get path
            file_path = temp_file.name
            img = read_image(file_path, uploaded_file.name.split('.')[-1])
            col1.header("Original Image")
            col1.image(img,use_column_width='always',clamp=True)   
            st.sidebar.button("Random augmentation", on_click=generate_augmentation)
            st.sidebar.button("Apply augmentation", on_click=apply_augmentation,args=([img, col2, user_dict]))

            # col1.button("Crop Image", on_click=function_here, args=([img]))

            pilImg = Image.open(file_path)
            with col1:
                cropped_img = st_cropper(pilImg, realtime_update=True, box_color='#0000FF', 
                                    aspect_ratio=None)
            st.write("Preview")
            # resize to original size
            #_ = cropped_img
            st.image(cropped_img)

            crop_button_clicked = st.button("Crop Image")

            # if crop_button_clicked:
            #     cropper_modal.open()

            # if cropper_modal.is_open():
            #     with cropper_modal.container():

    # uploaded_dict = st.empty()
    # When removing some translations from the randomly generated list -- it keeps them rather than updating the dictionary

    # Handle Crop Image View:
    # if crop_enabled == True:
    #     ...
    # Modal definition



if __name__ == '__main__':
    main()






    
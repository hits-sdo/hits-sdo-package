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
'''''''''
3/31 - Left off: downloading pickle file just fine, rendering is an issue (normalization?)
'''''''''

def button_augmentation_randomize(img):
    augment_list = AugmentationList(instrument = 'euv')
    augment_dict = augment_list.randomize()
    augments = Augmentations(img, augment_dict)
    augmented_img, title = augments.perform_augmentations()
    col2.header(title)
    col2.image(augmented_img,use_column_width='always',clamp=True)
    #a_img = pickle.dumps(augmented_img,open('augmented_img.p','wb'))
    a_img = pickle.dumps(augmented_img)
    col2.download_button(label="Download Augmented Image", data=a_img, file_name="augmented_img.p", mime="image/p")


st.header("Image Augmentation Tool")
uploaded_file = st.file_uploader("Choose an image...", type=["p", "jpg"])

if uploaded_file is not None:
    col1, col2 = st.columns([1,1])
    # img = read_image(uploaded_file)
#     because uploaded_file object doesn't have a path name attribute:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # write to temp file
        temp_file.write(uploaded_file.read())
        #get path
        file_path = temp_file.name
        img = read_image(file_path, uploaded_file.name.split('.')[-1])
        col1.header("Original Image")
        col1.image(img,use_column_width='always',clamp=True)

        st.button("Apply random augmentation", on_click=button_augmentation_randomize,args=([img]))


#img = read_image(uploaded_file)


    # pickle.dumps -> translates img to a bytestream

    # https://pythontic.com/modules/pickle/dumps

    # Problem:
    #   - Right now its 'uploaded_file', we want to download the 'augmented_image'
    #   - Need to download pickle file as well
    # # Convert the NumPy array to a Pillow Image object
    #img = Image.fromarray(augmented_img)
    # img = Image.fromarray(np.uint8(cm.gist_earth(augmented_img)*255)) (?) - Jasper
    # ^ do we need to colormap this? -Sierra --> I don't know :DD found it online - Jasper
    # That's what cm is doing. let's see! - SM
    # st.download_button(label='Download Image',
    #                     data= open('yourimage.png', 'rb').read(),
    #                     file_name='imagename.png',
    #                     mime='image/png')
#     from io import BytesIO
# buf = BytesIO()
# img.save(buf, format="JPEG")
# byte_im = buf.getvalue()
# Now you can use the st.download_button
#  
# btn = col.download_button(
#       label="Download Image",
#       data=byte_im,
#       file_name="imagename.png",
#       mime="image/jpeg",
#       )





    
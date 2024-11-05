import streamlit as st
import av
import cv2
from PIL import Image
import numpy as np
import datetime

st.title("Fortune-telling")

enable = st.checkbox("Enable camera")
img_file_buffer = st.camera_input("Take a picture", disabled=not enable)

if img_file_buffer:
    st.image(img_file_buffer)

if img_file_buffer is not None:
    img = Image.open(img_file_buffer)
    img_array = np.array(img)
    st.write(img_array.shape)

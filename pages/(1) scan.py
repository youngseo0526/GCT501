import streamlit as st
import numpy as np
from PIL import Image
from typing import Optional

SCAN_IMAGE_KEY = "scanned_img"
OUTPUT_IMAGE_KEY = "output_img"

st.title("Fortune-telling")

enable = st.checkbox("Enable camera")
img_file_buffer = st.camera_input("Take a picture", disabled=not enable)

def get_image(key: str) -> Optional[Image.Image]:
    if key in st.session_state:
        return st.session_state[key]
    return None

def set_image(key: str, img: Image.Image):
    st.session_state[key] = img

if img_file_buffer:
    img = Image.open(img_file_buffer)
    img_array = np.array(img)
    st.write(img_array.shape)
    #st.image(img)

    set_image(SCAN_IMAGE_KEY, img)

with st.sidebar:
    st.header("Scanned Image")
    scan_image = get_image(SCAN_IMAGE_KEY)
    if scan_image:
        st.image(scan_image)
    else:
        st.markdown("No image scanned yet")

    st.header("Generated Image")
    output_image = get_image(OUTPUT_IMAGE_KEY)  
    if output_image:
        st.image(output_image)  
    else:
        st.markdown("No image generated yet")

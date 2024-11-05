#!/usr/bin/env python

import streamlit as st
from gpt4allj import Model
st.set_page_config(layout='wide')
from streamlit_option_menu import option_menu
from PIL import Image
from typing import Optional

SCAN_IMAGE_KEY = "scanned_img"
LOADED_IMAGE_KEY = "loaded_image"
OUTPUT_IMAGE_KEY = "output_img"

def get_image(key: str) -> Optional[Image.Image]:
    if key in st.session_state:
        return st.session_state[key]
    return None

def set_image(key: str, img: Image.Image):
    st.session_state[key] = img


model = Model('./model/ggml-gpt4all-j.bin')

def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("Messages", value=str("\n".join(messages_str)), height=400)


st.markdown(""" <style> .font {
            font-size:30px ; font-family: 'Cooper Black'; color: #02ab21;} 
            </style> """, unsafe_allow_html=True)

BASE_PROMPT = [{"role": "AI", "content": "You are a helpful assistant."}]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

st.markdown(""" <style> .font {
                    font-size:30px ; font-family: 'Cooper Black'; color: #02ab21;} 
                    </style> """, unsafe_allow_html=True)
st.markdown('<p class="font">Fortune-telling</p>', unsafe_allow_html=True)

text = st.empty()
show_messages(text)

prompt = st.text_input("Prompt:", value="Enter your message here...")

col1, col2 = st.columns(2)
with col1:
    if st.button("Send"):
        with st.spinner("Generating response..."):
            st.session_state["messages"] += [{"role": "You", "content": prompt}]
            print(st.session_state["messages"][-1]["content"])
            message_response = model.generate(st.session_state["messages"][-1]["content"])
            st.session_state["messages"] += [
                {"role": "AI", "content": message_response}
            ]
            show_messages(text)
with col2:
    if st.button("Clear"):
        st.session_state["messages"] = BASE_PROMPT
        show_messages(text)

with st.sidebar:
    st.header("Scanned Image")
    scan_image = get_image(SCAN_IMAGE_KEY)
    if scan_image:
        st.image(scan_image)
    else:
        st.markdown("No image scanned yet")

    st.header("Generated Image")
    output_image = get_image(OUTPUT_IMAGE_KEY)  # Retrieve the generated image from session state
    if output_image:
        st.image(output_image)  # Display the generated image in the sidebar
    else:
        st.markdown("No image generated yet")

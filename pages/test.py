#!/usr/bin/env python

import streamlit as st
from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64
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

client = OpenAI(api_key="your_openai_api_key")    ######TODO#########

st.set_page_config(layout='wide')

def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("Messages", value="\n".join(messages_str), height=400)

# Custom CSS styling for Streamlit
st.markdown(""" 
<style> 
    .font { font-size:30px ; font-family: 'Cooper Black'; color: #02ab21; } 
</style> 
""", unsafe_allow_html=True)
st.markdown('<p class="font">Fortune-telling</p>', unsafe_allow_html=True)

# Initialize base prompt for the assistant
BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

# Display chat history
text = st.empty()
show_messages(text)

# Input prompt field for user
prompt = st.text_input("Prompt:", value="Enter your message here...")

col1, col2 = st.columns(2)
with col1:
    if st.button("Send"):
        with st.spinner("Generating response..."):
            # Append user message to session state
            st.session_state["messages"].append({"role": "user", "content": prompt})
            
            # Generate response using OpenAI API
            response = client.chat_completions.create(
                model="gpt-4",
                messages=st.session_state["messages"],
                max_tokens=300
            )
            
            # Extract the response content and update session state
            message_response = response.choices[0].message["content"]
            st.session_state["messages"].append({"role": "assistant", "content": message_response})
            
            # Display updated chat history
            show_messages(text)

with col2:
    if st.button("Clear"):
        # Clear chat history and reset to base prompt
        st.session_state["messages"] = BASE_PROMPT
        show_messages(text)

# Function to handle image file uploads
def image_uploader(prefix):
    image = st.file_uploader("Upload an Image", type=["jpg", "png"], key=f"{prefix}-uploader")
    if image:
        image = Image.open(image)
        print(f"Loaded input image of size ({image.width}, {image.height})")
        return image
    return None

# Display the image uploader and process the uploaded image
uploaded_image = image_uploader("image")
if uploaded_image:
    # Display uploaded image
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    # Convert image to base64 for OpenAI API compatibility if needed
    buffered = BytesIO()
    uploaded_image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    if st.button("Describe Image"):
        with st.spinner("Describing image..."):
            # Add image description request to messages
            st.session_state["messages"].append({
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {"type": "image_base64", "image_base64": img_base64}
                ]
            })
            
            # Generate response for image description
            response = client.chat_completions.create(
                model="gpt-4",
                messages=st.session_state["messages"],
                max_tokens=300
            )
            
            # Display the assistant's image description response
            description_response = response.choices[0].message["content"]
            st.session_state["messages"].append({"role": "assistant", "content": description_response})
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

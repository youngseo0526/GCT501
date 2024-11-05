from typing import Optional

import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

from model.sd2_generate import PIPELINE_NAMES, generate, SD_20, SD_21, SD_XL_TURBO, SD_XL_10, SD_XL_10_REFINER


DEFAULT_PROMPT = "tarot card style, high-quality"
DEFAULT_WIDTH, DEFAULT_HEIGHT = 512, 512
SCAN_IMAGE_KEY = "scanned_img"
OUTPUT_IMAGE_KEY = "output_img"
LOADED_IMAGE_KEY = "loaded_image"


def get_image(key: str) -> Optional[Image.Image]:
    if key in st.session_state:
        return st.session_state[key]
    return None


def set_image(key: str, img: Image.Image):
    st.session_state[key] = img

    
def prompt_and_generate_button(prefix, pipeline_name: PIPELINE_NAMES, **kwargs):
    prompt = st.text_area(
        "Prompt",
        value=DEFAULT_PROMPT,
        key=f"{prefix}-prompt",
    )
    negative_prompt = st.text_area(
        "Negative prompt",
        value="",
        key=f"{prefix}-negative-prompt",
    )
    col1, col2 = st.columns(2)
    with col1:
        steps = st.slider(
            "Number of inference steps",
            min_value=1,
            max_value=200,
            value=20,
            key=f"{prefix}-inference-steps",
        )
    with col2:
        guidance_scale = st.slider(
            "Guidance scale",
            min_value=0.0,
            max_value=20.0,
            value=7.5,
            step=0.5,
            key=f"{prefix}-guidance-scale",
        )
    enable_attention_slicing = st.checkbox(
        "Enable attention slicing (enables higher resolutions but is slower)",
        key=f"{prefix}-attention-slicing",
    )
    enable_cpu_offload = st.checkbox(
        "Enable CPU offload (if you run out of memory, e.g. for XL model)",
        key=f"{prefix}-cpu-offload",
        value=False,
    )

    if st.button("Generate image", key=f"{prefix}-btn"):
        with st.spinner("Generating image..."):
            image = generate(
                prompt,
                pipeline_name,
                negative_prompt=negative_prompt,
                steps=steps,
                guidance_scale=guidance_scale,
                enable_attention_slicing=enable_attention_slicing,
                enable_cpu_offload=enable_cpu_offload,
                **kwargs,
            )
            set_image(OUTPUT_IMAGE_KEY, image.copy())
        st.image(image)


def width_and_height_sliders(prefix):
    col1, col2 = st.columns(2)
    with col1:
        width = st.slider(
            "Width",
            min_value=64,
            max_value=1600,
            step=16,
            value=768,
            key=f"{prefix}-width",
        )
    with col2:
        height = st.slider(
            "Height",
            min_value=64,
            max_value=1600,
            step=16,
            value=768,
            key=f"{prefix}-height",
        )
    return width, height


def image_uploader(prefix):
    image = st.file_uploader("Image", ["jpg", "png"], key=f"{prefix}-uploader")
    if image:
        image = Image.open(image)
        print(f"loaded input image of size ({image.width}, {image.height})")
        return image

    return get_image(LOADED_IMAGE_KEY)


def img2img_tab():
    prefix = "img2img"
    col1, col2 = st.columns(2)

    with col1:
        image = image_uploader(prefix)
        if image:
            st.image(image)

    with col2:
        if image:
            version = st.selectbox(
                "Model version", [SD_21, SD_XL_10_REFINER], key=f"{prefix}-version"
            )
            strength = st.slider(
                "Strength (1.0 ignores the existing image so it's not a useful value)",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.05,
                key=f"{prefix}-strength",
            )
            prompt_and_generate_button(
                prefix, "img2img", image_input=image, version=version, strength=strength
            )


def main():
    st.set_page_config(layout="wide")
    st.title("Stable Diffusion 2.0/2.1/XL Simple Playground")

    prefix = "img2img"
    col1, col2 = st.columns(2)

    with col1:
        image = image_uploader(prefix)
        if image:
            st.image(image)

    with col2:
        if image:
            version = st.selectbox(
                "Model version", [SD_21, SD_XL_10_REFINER], key=f"{prefix}-version"
            )
            strength = st.slider(
                "Strength (1.0 ignores the existing image so it's not a useful value)",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.05,
                key=f"{prefix}-strength",
            )
            prompt_and_generate_button(
                prefix, "img2img", image_input=image, version=version, strength=strength
            )

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


if __name__ == "__main__":
    main()

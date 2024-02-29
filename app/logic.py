import os
import random
from collections import defaultdict

import streamlit as st
from streamlit_image_select import image_select

from .horoscope import REPO_ROOT_DIR


def initialize_session_state():
    state_objects = {
        "picture_taken":    False,
        "image_filepaths":  None,
        "recommendation":   recursive_default_dict(),
    }

    for obj, value in state_objects.items():
        if obj not in st.session_state:
            st.session_state[obj] = value


def recursive_default_dict():
    return defaultdict(recursive_default_dict)



def randomly_select_images():
        filepath = REPO_ROOT_DIR / "img"
        img_fps = os.listdir(filepath)
        exts = ["jpeg", "png"]
        img_fps = [filepath/fn for fn in img_fps if fn.split(".")[-1] in exts]
        img_fps = random.sample(img_fps, 4)
        st.session_state["image_filepaths"] = img_fps


def choose_your_style():
    if st.session_state["image_filepaths"] is None:
         randomly_select_images()

    label = "Next, which of these images best captures your style?"
    st.markdown(f"#### {label}")
    img_fps = st.session_state["image_filepaths"]
    selection = image_select("Select a picture", img_fps)
    style = image_filename_to_sytle_descriptor(selection)
    return style


def image_filename_to_sytle_descriptor(filepath):
     basename = os.path.basename(filepath)
     filename = basename.split(".")[0]
     
     descriptors = {
        "audrey-hepburn-sq":    "Audrey Hepburn in Breakfast at Tiffany's",
        "barn":                 "rustic, country-style living", 
        "hiking-couple-sq":     "outdoorsy, crunchy, hiking lifestyle", 
        "jon-hamm-sq":          "Handsome, well-dressed Jon Hamm",  
        "lulu-sq":              "sportsy, athletic, athleisure lifestyle",  
        "rainbow-dash-sq":      "Rainbow Dash from My Little Pony",
        "spiderman-sq":         "Spiderman", 
        }
     style = descriptors[filename]
     return style


def display_glasses_recommendation(month, day, style_descriptor):
    glasses_dir = REPO_ROOT_DIR / "data/spectacles"
    
    filename = st.session_state["recommendation"][style_descriptor][month][day]
    if not isinstance(filename, str):
        glasses = os.listdir(glasses_dir)
        glasses = [fp for fp in glasses if fp.split(".")[-1] == "png"]
        st.session_state["recommendation"][style_descriptor][month][day] = random.choice(glasses)
    
    st.markdown("#### Your Recommended Frames")
    filename = st.session_state["recommendation"][style_descriptor][month][day]
    filepath = glasses_dir / filename
    st.image(str(filepath))


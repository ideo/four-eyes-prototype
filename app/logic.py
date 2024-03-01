import os
import random
from collections import defaultdict

import streamlit as st
from streamlit_image_select import image_select

from .horoscope import REPO_ROOT_DIR
from .image_processing import extract_likely_birthday


def initialize_session_state():
    state_objects = {
        "picture_taken":    False,
        "image_filepaths":  None,
        "recommendation":   recursive_default_dict(),
    }

    for obj, value in state_objects.items():
        if obj not in st.session_state:
            st.session_state[obj] = value


def backup_birthday_selector():
    col1, col2 = st.columns(2)
    with col1:
        month = st.selectbox("Month", options=[""] + list(range(1,13)))
        month = month if month != "" else None
    with col2:
        day = st.selectbox("Day", options=[""] + list(range(1,32)))
        day = day if day != "" else None

    birthday = None
    if month is not None and day is not None:
        month, day, birthday = extract_likely_birthday([f"{month}/{day}/2024"])
        print(birthday)

    return month, day, birthday


def recursive_default_dict():
    return defaultdict(recursive_default_dict)


def randomly_select_images():
        filepath = REPO_ROOT_DIR / "img"
        img_fps = os.listdir(filepath)
        img_fps = [filepath/fn for fn in img_fps if fn.split(".")[-1] != "DS_Store"]
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
        "cubism":                  "the cubist art movement",
        "dali":                    "the painting style of Salvador Dalí",
        "georgia-okeefe":          "the floral landscapes of Georgia O'Keeffe",
        "impressionism":           "the pioneering spirit of impressionist painters",
        "jackson-pollack":         "the vibrant quantities of Jackson Pollack",
        "modernist-photography":   "modernist architecture",
        "mondrian":                "regularity and symmetry of Modrian-eque paintings",
        "romanticism":             "the classicism and timelessness of romantic paintings",
        }
     style = descriptors[filename]
     return style


def display_glasses_recommendation(month, day, style_descriptor):
    glasses_dir = REPO_ROOT_DIR / "data/spectacles"
    
    filename = st.session_state["recommendation"][style_descriptor][month][day]
    if not isinstance(filename, str):
        glasses = os.listdir(glasses_dir)
        glasses = [fp for fp in glasses if fp.split(".")[-1] == "png"]
        st.session_state["recommendation"][style_descriptor][month][day] = random.sample(glasses, 4)
    
    st.markdown("#### Your Recommended Frames")
    filenames = st.session_state["recommendation"][style_descriptor][month][day]
    filepath = lambda fn: str(glasses_dir / fn)

    col1, col2 = st.columns(2)
    with col1:
        st.image(filepath(filenames[0]))
        st.image(filepath(filenames[1]))
    with col2:
        st.image(filepath(filenames[2]))
        st.image(filepath(filenames[3]))


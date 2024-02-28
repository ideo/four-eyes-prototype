import streamlit as st


def initialize_session_state():
    state_objects = {
        "picture_taken":    False,
    }
    for obj, value in state_objects.items():
        if obj not in st.session_state:
            st.session_state[obj] = value
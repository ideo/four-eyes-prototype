import streamlit as st


def initialize_session_state():
    state_objects = {
        "picture_taken":    False,
    }
    for obj, value in state_objects.items():
        if obj not in st.session_state:
            st.session_state[obj] = value


# def take_a_picture():
#     if not st.session_state["picture_taken"]:
#         picture = st.camera_input("Take a picture", key="camera_input")
#         if picture:
#             st.session_state["picture_taken"]
#             return picture

#     else:
#         _, cntr, _ = st.columns([5,3,5])
#         with cntr:
#             clicked = st.button("Retake Picture") 
#             if clicked:
#                 st.session_state["picture_taken"] = False

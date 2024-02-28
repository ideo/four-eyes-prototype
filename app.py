import streamlit as st

from app import logic as lg
from app import image_processing as image
from app.horoscope import horoscope


st.set_page_config(
    page_title="AstroLens",
    page_icon="👓"
)

lg.initialize_session_state()


st.title("AstroLens")
label = "Take a picture of your ID. Make sure your birthday clearly visible."
picture = st.camera_input(label)

if picture:
    text = image.extract_text_from_image(picture)
    dates = image.recognize_dates(text)
    birthday = image.extract_likely_birthday(dates)

    if birthday is not None:
        st.header(birthday)
        with st.spinner("Reading the stars..."):
            response = horoscope(birthday)
            st.write(response.content)

    else:
        picture = None
        st.warning("Oh no! I can't find your birthday. Please take a new picture.")
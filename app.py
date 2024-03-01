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
label = "Take a picture of your ID or insurance card. Make sure your birthday clearly visible."
picture = st.camera_input(label)

if picture is None:
    st.write("If the photo is too blurry, holding your phone still for a few seconds can help it snap into focus.")

if picture:
    text = image.extract_text_from_image(picture)
    dates = image.recognize_dates(text)
    month, day, birthday = image.extract_likely_birthday(dates)

    if birthday is None:
        st.warning("Oh no! I can't find your birthday. Please take a new picture, or input your birthday below.")
        month, day, birthday = lg.backup_birthday_selector()

    if birthday is not None:
        # st.header(birthday)

        st.write("")
        style_descriptor = lg.choose_your_style()
        
        if style_descriptor is not None:

            with st.spinner("Reading the stars..."):
                st.write("")
                st.markdown("#### Your AstroLens Horoscope")
                response = horoscope(birthday, style_descriptor)
                st.write(response.content)

                st.write("")
                lg.display_glasses_recommendation(month, day, style_descriptor)

    else:
        picture = None
        



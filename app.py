import streamlit as st
import pytesseract
from pytesseract import Output
from PIL import Image
import cv2

from app import logic as lg
from app import image_processing as image
from app.horoscope import horoscope


lg.initialize_session_state()


st.title("HoroLens")
picture = st.camera_input("Take a Picture")
# picture = Image.open("data/IMG_8769.JPG")

if picture:
    text = image.extract_text_from_image(picture)

    # text = [
    #     "Cigna Health and Life Insurance Co. Coverage Effective Date: 01/01/2024",
    #     "Group: 3343029",
    #     "ID: U80060737 01 Name: Joe Gambino",
    #     "5 Jesse White + Secretary of FeseatLinieapply aduc no:6515-4829-1 22¢ 3 pes:08/03/1994 & weer 08/03/2025. |",
    #     "pos:08/03/1991 «exe 08/03/20",
    #     "wducno:6515-48 29-4 neo = % vos:08/03/1994 av exe: 08/03/2025.",
    # ]

    # st.write(text)

    dates = image.recognize_dates(text)
    birthday = image.extract_likely_birthday(dates)

    if birthday is not None:
        st.header(birthday)
        with st.spinner("Reading the stars..."):
            response = horoscope(birthday)
            st.write(response.content)

    else:
        picture = None
        st.success("Oh no! I can't find your birthday. Please take a new picture.")
import re
from itertools import chain
from datetime import datetime
# from collections import Counter

import cv2
from PIL import Image
import pytesseract as tesseract
# from pytesseract import Output
import numpy as np
import inflect

ENGINE = inflect.engine()


def convert_to_grayscale(picture):
    img = Image.open(picture)
    # img = picture
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


def extract_text_from_image(picture):
    img = convert_to_grayscale(picture)
    text = tesseract.image_to_string(img)
    text = [txt for txt in text.split("\n") if txt != ""]
    return text


def recognize_dates(text):
    date_pattern = "[0-9]+/[0-9]+/[0-9]+"
    matches = [re.findall(date_pattern, txt) for txt in text]
    dates = list(chain.from_iterable([match for match in matches if match]))
    return dates


def extract_likely_birthday(dates):
    month_days = [(dt.split("/")[0], dt.split("/")[1]) for dt in dates]
    month, day = max(month_days, key=month_days.count)
    month, day = int(month), int(day)
    birthday = datetime(year=2000, month=month, day=day).strftime("%B")
    birthday += f" {ENGINE.ordinal(day)}"
    return birthday

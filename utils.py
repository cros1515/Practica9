# utils.py

import base64
import os
import streamlit as st
from config import BACKGROUND_IMAGE

def add_bg_from_local(image_file=BACKGROUND_IMAGE):
    if os.path.exists(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/{"jpg"};base64,{encoded_string});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

from main import readImage

import streamlit as st
from PIL import Image

incon = st.container()
outcon = st.container()

with incon:
    yourage = st.number_input("Age", step=1)
    yourfile = st.file_uploader("Upload a file",type=["png","jpg"])

    if yourfile is not None:
        yourimage = Image.open(yourfile)
        st.image(yourimage)
        with outcon:
            st.write(readImage(yourfile.name))
        
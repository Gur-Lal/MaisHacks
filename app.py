from main import readImage

import os
import streamlit as st
from PIL import Image


st.title("Nutrition Label Reader")

incon = st.container()
outcon = st.container()

with incon:
    yourname = st.text_input("Name")
    yourage = st.number_input("Age", step=1)
    yourweight = st.number_input("Weight (kg)", step=1)
    
    yourfile = st.file_uploader("Upload a file",type=["png","jpg"])

    if yourfile is not None:
        save_path = f"uploads/{yourfile.name}"

        with open(save_path, "wb") as f:
            f.write(yourfile.read())
            
        yourimage = Image.open(yourfile)
        
        st.image(yourimage)

        with outcon:
            st.write(readImage(yourfile.name))
        

# clear uploaded files
for fname in os.listdir("uploads"):
    fpath = os.path.join("uploads", fname)
    if os.path.isfile(fpath):
        os.remove(fpath)
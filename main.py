import streamlit as st
from PIL import Image
import cv2
import pytesseract
from re import search
import numpy as np
import os

# Setting the path for Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def readImage(image):
    # Convert PIL Image to OpenCV format
    img_cv = np.array(image)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

    # Preprocessing
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, img_cv = cv2.threshold(img_cv, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    readData = pytesseract.image_to_string(img_cv, lang='eng', config='--psm 6')

    calories = fat = sodium = sugars = Protein = -1

    lineData = readData.splitlines()
    for line in lineData:
        if 'Calories' in line:
            try:
                calories = int(search(r'\d+', line).group())
                if (calories < 9):
                    calories = -1
            except:
                pass
        elif 'Fat' in line or 'Lipides' in line:
            try:
                fat = int(search(r'\d+', line).group())
            except:
                pass
        elif 'Sodium' in line:
            try:
                sodium = int(search(r'\d+', line).group())
                if (sodium < 5):
                    sodium = -1
            except:
                pass
        elif 'Sugars' in line or 'Sucres' in line:
            try:
                sugars = int(search(r'\d+', line).group())
            except:
                pass
        elif 'Protein' in line or 'Proteines' in line:
            try:
                Protein = int(search(r'\d+', line).group())
            except:
                pass

    dictFood = {
        "Calories": calories,
        "Fat": fat,
        "Sodium": sodium,
        "Sugars": sugars,
        "Protein": Protein
    }
    return dictFood

plastic_recycling_info = {
    '1': {
        'type': 'PETE or PET (Polyethylene Terephthalate)',
        'info': 'Recyclable: Mostly recycled; used to make bottles, etc.'
    },
    '2': {
        'type': 'HDPE (High-Density Polyethylene)',
        'info': 'Recyclable: Commonly recycled; used for milk jugs, etc.'
    },
    # Add all the other plastic types and their information
    # ...
}



def is_healthy_food(dictFood, weight, age):
    calories = dictFood["Calories"]
    fat = dictFood["Fat"]
    sodium = dictFood["Sodium"]
    protein = dictFood["Protein"]

    if calories <= 0 or fat < 0 or sodium < 0 or protein < 0:
        st.warning("Incomplete or incorrect nutrition information.")
        return False
    
    fat_calories = fat * 9
    protein_calories = protein * 4
    
    fat_percentage = (fat_calories / calories) * 100
    protein_percentage = (protein_calories / calories) * 100
    
    # Age-dependent Sodium thresholds
    sodium_lower = 1500 if age < 50 else 1300
    sodium_upper = 2300 if age < 50 else 2000
    
    if (20 <= fat_percentage <= 35) and (10 <= protein_percentage <= 35) and (sodium_lower <= sodium <= sodium_upper):
        return True
    else:
        return False

# Streamlit UI
st.title("Nutrition Information Extractor")
st.write('---')

# Improved layout with columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter Your Details")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
    weight = st.number_input("Weight (in kg)", min_value=1.0, max_value=200.0, value=70.0, step=0.1)
    
with col2:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader("Choose an image to check its nutrition...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    save_path = f"uploads/{uploaded_file.name}"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    st.write("Processing...")

    results = readImage(image)
    
    st.write("Here are the extracted nutrition details:")
    st.json(results)
    
    if is_healthy_food(results, weight, age):  # Remember to pass age here
        st.success("This seems like a healthy food choice for you!")
    else:
        st.warning("This might not be the healthiest choice for you. Consider something lighter!")


st.write('---')
st.markdown("For detailed nutritional guidelines, please refer to [Canada's Dietary Guidelines](https://www.canada.ca/en/health-canada/services/food-nutrition/healthy-eating/dietary-reference-intakes/tables/reference-values-macronutrients-dietary-reference-intakes-tables-2005.html)")

# clear uploaded files
for fname in os.listdir("uploads"):
    fpath = os.path.join("uploads", fname)
    if os.path.isfile(fpath):
        os.remove(fpath)

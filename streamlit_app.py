# Import section
import os
import streamlit as st
from PIL import Image
import cv2
import pytesseract
from re import search
import numpy as np

# Title & Icon
st.set_page_config(page_title='Nutrition Information Extractor', page_icon=':apple:')

# Add logo at the top
logo_path = "logo_noBackground.png"
st.image(logo_path, width=200)  # Adjust width as needed

# Add team information in the sidebar
st.sidebar.header('Team Members')

team_members = {
    'Syed Bilal Afzal': 'Bilal is a U1 computer engineering Student at Mcgill and is interested in making a positive impact on your health!',
    'Gur Lal': 'Gur is a U1 software engineering at Concordia. He\'s passionate about AI and space.',
    'Mona Liu': 'Mona is a U0 student hoping to pursue computer science. This is her first time working with AI. She loves design and helping others.',
    'Jiucheng Zang': 'Jiucheng is a U0 computer science student at University of Waterloo. He loves tinkering with AI in his free time'
}

for member, info in team_members.items():
    st.sidebar.subheader(member)
    st.sidebar.write(info)

# Setting the path for Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def readImage(image):
    img_cv = np.array(image)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, img_cv = cv2.threshold(img_cv, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    readData = pytesseract.image_to_string(img_cv, lang='eng', config='--psm 6')
    dictFood = {"Calories": -1, "Fat": -1, "Sodium": -1, "Sugars": -1, "Protein": -1}

    for line in readData.splitlines():
        try:
            if 'Calories' in line:
                dictFood['Calories'] = int(search(r'\d+', line).group())
            elif 'Fat' in line or 'Lipides' in line:
                dictFood['Fat'] = int(search(r'\d+', line).group())
            elif 'Sodium' in line:
                dictFood['Sodium'] = int(search(r'\d+', line).group())
            elif 'Sugars' in line or 'Sucres' in line:
                dictFood['Sugars'] = int(search(r'\d+', line).group())
            elif 'Protein' in line or 'Proteines' in line:
                dictFood['Protein'] = int(search(r'\d+', line).group())
        except:
            pass
    return dictFood

def is_healthy_food(dictFood, weight, age):
    calories, fat, sodium, sugars, protein = dictFood.values()

    if calories <= 0 or fat < 0 or sodium < 0 or protein < 0:
        st.warning("Incomplete or incorrect nutrition information.")
        return False

    fat_calories = fat * 9
    protein_calories = protein * 4
    fat_percentage = (fat_calories / calories) * 100
    protein_percentage = (protein_calories / calories) * 100
    sodium_lower = 1500 if age < 50 else 1300
    sodium_upper = 2300 if age < 50 else 2000

    return 20 <= fat_percentage <= 35 and 10 <= protein_percentage <= 35 and sodium_lower <= sodium <= sodium_upper

st.title("Wise Bite - The Nutrition Information Extractor")
st.subheader('From Binary to Dietary - We\'ve Got You Covered!')
st.write('---')

col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter Your Details")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
    weight = st.number_input("Weight (in kg)", min_value=1.0, max_value=200.0, value=70.0, step=0.1)


with col2:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    save_path = f"uploads/{uploaded_file.name}"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    with st.spinner("Processing..."):
        results = readImage(image)
        st.write("Extracted nutrition details:")
        st.json(results)

    if is_healthy_food(results, weight, age):
        st.success("This seems like a healthy food choice for you!")
    else:
        st.warning("This might not be the healthiest choice for you. Consider something lighter!")

st.write('---')
st.markdown("For detailed nutritional guidelines, please refer to [Canada's Dietary Guidelines](https://www.canada.ca/en/health-canada/services/food-nutrition/healthy-eating/dietary-reference-intakes/tables/reference-values-macronutrients-dietary-reference-intakes-tables-2005.html)")

for fname in os.listdir("uploads"):
    fpath = os.path.join("uploads", fname)
    #if os.path.isfile(fpath):
        #os.remove(fpath)
import streamlit as st
from PIL import Image
import cv2
import pytesseract
from re import search

# Setting the path for Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def readImage(img_path):
    img_cv = cv2.imread(img_path)
    readData = pytesseract.image_to_string(img_cv, lang='eng')

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

def is_healthy_food(dictFood, weight):
    if dictFood["Calories"] > 500 and weight > 70:
        return False
    return True

# Streamlit UI
st.title("Nutrition Information Extractor")

# User details input
st.subheader("Enter Your Details")
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=120)
weight = st.number_input("Weight (in kg)", min_value=1.0, max_value=200.0)

uploaded_file = st.file_uploader("Choose an image to check its nutrition...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    st.write("Processing...")

    # Save the uploaded image to a temporary location
    temp_path = r"C:\Users\zixin.deng\OneDrive - Vffice\Desktop\MAISPROJECT\temp_img.jpg"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    results = readImage(temp_path)

    st.write("Here are the extracted nutrition details:")
    st.json(results)

    if is_healthy_food(results, weight):
        st.success("This seems like a healthy food choice for you!")
    else:
        st.warning("This might not be the healthiest choice for you. Consider something lighter!")

from sys import argv, exit
from cv2 import imread, cvtColor, COLOR_BGR2RGB
import pytesseract
from re import search   
from os import system

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'


def readImage(src):
    img_cv = imread(f"uploads/{src}")
    # img_cv = cvtColor(img_cv, COLOR_BGR2RGB)
    readData = pytesseract.image_to_string(img_cv, lang='eng')

    calories = fat = sodium = sugars = Protein = -1

    lineData = readData.splitlines()
    for line in lineData:
        if 'Calories' in line or 'Calories' in line:
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

        elif 'Sodium' in line or 'Sodium' in line:
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
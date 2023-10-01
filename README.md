# Wise Bite - The Nutrition Information Extractor

## Overview:
Wise Bite is a cutting-edge nutrition information extractor that transforms the way you perceive and consume food. It analyzes the nutritional content of food items and provides you with actionable insights to make healthier food choices.

## Features:
- **User-Friendly Interface:** A seamless and intuitive interface that allows users to easily input their details and upload images of food items.
- **Nutritional Analysis:** Extracts nutritional information such as Calories, Fat, Sodium, Sugars, and Protein from the uploaded images.
- **Health Assessment:** Based on the extracted nutrition details, it provides an immediate health assessment, advising if the chosen food item is a healthy choice for the user.
- **Personalized Advice:** Offers personalized nutritional advice through integration with OpenAI's GPT-3.5-turbo, acting as a personal nutritional specialist.
- **Ask Gitana:** A feature where users can ask for more health advice and receive responses based on their queries.

## How to Use:
1. **Enter Your Details:** Fill in your name, age, and weight in the respective fields.
2. **Upload Image:** Upload an image of the food item whose nutritional information you want to extract.
3. **View Extracted Information:** After uploading, view the extracted nutritional details and receive immediate health assessments and advice.
4. **Ask for More Advice:** Utilize the 'Ask Gitana' feature for more personalized health and nutritional advice.

## Technology Stack:
- **Streamlit:** For creating the web app interface.
- **OpenAI (GPT-3.5-turbo):** For generating personalized nutritional advice.
- **PyTesseract:** For extracting text from images.
- **OpenCV & PIL:** For image processing.
- **Python:** The backend is powered by Python, utilizing its extensive libraries and frameworks.

## Setup and Installation:
1. Ensure you have Python installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory and install the required packages using pip:
   ```sh
   pip install -r requirements.txt

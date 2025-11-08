# Swiggy Restaurant Recommendation System

## Overview

This project is a **Streamlit-based web application** that recommends
restaurants to users based on: - City and Area\
- Cuisine preference
- Rating and Cost filters

It uses **cosine similarity** on encoded restaurant data to suggest the
most similar restaurants.

------------------------------------------------------------------------

## Features

-   Bilingual Interface (English & Tamil)
-   User-friendly filters for city, area, cuisine, rating, and cost
-   Dynamic results with restaurant cards
-   Elegant UI with gradient background and styled sidebar
-   Smart recommendations using **Cosine Similarity**

------------------------------------------------------------------------

## Project Structure

    Swiggy_Restaurant_Recommendation_System/
    │
    ├── cleaned_data.csv          # Original restaurant data
    ├── encoder_data.csv          # Encoded numerical data for similarity
    ├── app.py                    # Main Streamlit application
    ├── requirements.txt          # Python dependencies
    └── README.md                 # Project documentation (this file)

------------------------------------------------------------------------

## Setup Instructions

### 1. Clone or Download the Project

``` bash
git clone https://github.com/udhayakumar-coder/Swiggy_Recommendation.git
cd Swiggy_Restaurant_Recommendation_System
```

### 2. Install Dependencies

Create a virtual environment (optional) and install requirements:

``` bash
pip install -r requirements.txt
```

**requirements.txt**

    streamlit
    pandas
    numpy
    scikit-learn

------------------------------------------------------------------------

### 3. Run the App

``` bash
streamlit run recommend_app.py
```

------------------------------------------------------------------------

## File Paths

In `app.py`, update the paths:

``` python
cleaned_path = r"F:\Project\Swiggy_Restaurant_Recommendation_System_using_Streamli\cleaned_data.csv"
encoded_path = r"F:\Project\Swiggy_Restaurant_Recommendation_System_using_Streamli\encoder_data.csv"
```

Make sure these files exist in the same directory or update the paths as
needed.

------------------------------------------------------------------------

## How It Works

1.  Loads the cleaned and encoded datasets\
2.  Filters restaurants based on selected city, area, cuisine, rating,
    and cost\
3.  Uses **Cosine Similarity** to compute similarity scores\
4.  Displays the top recommended restaurants with details

------------------------------------------------------------------------

## Tamil Description (தமிழ் விளக்கம்)

இந்த திட்டம் **Streamlit** அடிப்படையிலான உணவக பரிந்துரை செயலியாகும்.\
நகரம், பகுதி, உணவுவகை, மதிப்பீடு, செலவு ஆகியவற்றின் அடிப்படையில்\
உங்களுக்கான சிறந்த உணவகங்களை பரிந்துரைக்கிறது.

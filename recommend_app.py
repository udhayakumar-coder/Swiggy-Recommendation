import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# -----------------------------------------------------
# Page Setup
# -----------------------------------------------------
st.set_page_config(page_title="🍽️ Swiggy Restaurant Recommender", layout="wide")

# -----------------------------------------------------
# Custom Style (Solid Sidebar + Nice Background)
# -----------------------------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f0f4f8;
    background-image: linear-gradient(to bottom right, #f0f4f8, #d9e2ec);
}
[data-testid="stSidebar"] {
    background-color: #00695C;  /* Teal Green */
    color: white;
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
    color: white !important;
}
.title {
    color: #1a237e;
    text-align: center;
    font-size: 36px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #555;
    font-size: 18px;
    margin-bottom: 35px;
}
.stButton>button {
    background-color: #0077b6;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
.stButton>button:hover {
    background-color: #0096c7;
}
.restaurant-card {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# Header Section
# -----------------------------------------------------
st.markdown("<div class='title'>🍴 Swiggy Restaurant Recommendation System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Find your favorite restaurants (உங்கள் விருப்பமான உணவகங்களைத் தேடுங்கள்)</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------
@st.cache_data
def load_data():
    cleaned_path = r"F:\Project\Swiggy_Restaurant_Recommendation_System_using_Streamli\cleaned_data.csv"
    encoded_path = r"F:\Project\Swiggy_Restaurant_Recommendation_System_using_Streamli\encoder_data.csv"

    if not os.path.exists(cleaned_path) or not os.path.exists(encoded_path):
        st.error("CSV files not found. Please check the file paths.")
        st.stop()

    cl_df = pd.read_csv(cleaned_path, index_col=0)
    en_df = pd.read_csv(encoded_path, index_col=0)

    # Remove "Unknown" area rows
    if "Area" in cl_df.columns:
        cl_df = cl_df[cl_df["Area"].str.lower() != "unknown"]

    return cl_df, en_df

cl_df, en_df = load_data()

# -----------------------------------------------------
# Recommendation Function
# -----------------------------------------------------
def get_restaurants(city, area, cuisines, min_rating, max_cost, top_n=10):
    city_df = cl_df[cl_df["City"].str.lower() == city.lower()]
    if area != "All Areas":
        city_df = city_df[city_df["Area"].str.lower() == area.lower()]
    if city_df.empty:
        return pd.DataFrame()

    if cuisines:
        city_df = city_df[city_df["cuisine"].str.lower().isin([c.lower() for c in cuisines])]

    city_df = city_df[(city_df["rating"] >= min_rating) & (city_df["cost"] <= max_cost)]
    if city_df.empty:
        return pd.DataFrame()

    city_encoded = en_df.loc[city_df.index]
    sim_matrix = cosine_similarity(city_encoded)
    mean_similarity = sim_matrix.mean(axis=0)
    sorted_idx = np.argsort(mean_similarity)[::-1]
    similar_restaurants = city_df.iloc[sorted_idx].head(top_n).copy()
    similar_restaurants["similarity_score"] = mean_similarity[sorted_idx][:top_n]

    return similar_restaurants.reset_index(drop=True)

# -----------------------------------------------------
# Sidebar (Filters + Language)
# -----------------------------------------------------
left, right = st.columns([1, 2])

with left:
    lang = st.radio("🌐 Language / மொழி தேர்வு", ["English", "தமிழ்"])

    cities = sorted(cl_df["City"].dropna().unique())
    city_choice = st.selectbox("Select City" if lang == "English" else "நகரம் தேர்வு செய்யவும்", cities)

    areas = cl_df[cl_df["City"] == city_choice]["Area"].dropna().unique().tolist()
    if len(areas) > 1:
        areas.insert(0, "All Areas")
    area_choice = st.selectbox("Select Area" if lang == "English" else "பகுதி தேர்வு செய்யவும்", areas)

    if area_choice == "All Areas":
        cuisines = sorted(cl_df[cl_df["City"] == city_choice]["cuisine"].dropna().unique())
    else:
        cuisines = sorted(cl_df[
            (cl_df["City"] == city_choice) &
            (cl_df["Area"] == area_choice)
        ]["cuisine"].dropna().unique())

    cuisine_choices = st.multiselect("Select Cuisine(s)" if lang == "English" else "உணவுவகைகள் தேர்வு செய்யவும்", cuisines)
    min_rating = st.slider("Minimum Rating ⭐" if lang == "English" else "குறைந்தபட்ச மதிப்பீடு ⭐", 0.0, 5.0, 3.5, 0.1)
    max_cost = st.slider("Maximum Cost (₹)" if lang == "English" else "அதிகபட்ச செலவு (₹)", 100, 2000, 800, 50)
    top_n = st.slider("Number of Recommendations" if lang == "English" else "பரிந்துரைகள் எண்ணிக்கை", 5, 20, 10)
    find_btn = st.button("✨ Find Restaurants" if lang == "English" else "✨ உணவகங்களை காண்க")

# -----------------------------------------------------
# Display Results
# -----------------------------------------------------
with right:
    if find_btn:
        results = get_restaurants(city_choice, area_choice, cuisine_choices, min_rating, max_cost, top_n)

        if results.empty:
            msg = "No matching restaurants found for your selection." if lang == "English" else "உங்கள் தேர்வுக்கு பொருந்தும் உணவகங்கள் எதுவும் இல்லை."
            st.warning(msg)
        else:
            if lang == "English":
                st.subheader(f"🍽️ Top {len(results)} Recommended Restaurants in {city_choice} ({area_choice})")
            else:
                st.subheader(f"🍽️ {city_choice} - {area_choice} பகுதியில் சிறந்த {len(results)} உணவகங்கள்")

            for _, row in results.iterrows():
                name = row['name']
                rating = row['rating']
                count = int(row['rating_count'])
                cost = row['cost']
                cuisine = row['cuisine']
                area = row.get('Area', '')

                if lang == "English":
                    st.markdown(
                        f"""
                        <div class='restaurant-card'>
                            <h4>🏠 {name}</h4>
                            <p><strong>⭐ Rating:</strong> {rating} ({count} reviews)</p>
                            <p><strong>💸 Cost for Two:</strong> ₹{cost}</p>
                            <p><strong>🍜 Cuisine:</strong> {cuisine}</p>
                            <p><strong>📍 Area:</strong> {area}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(
                        f"""
                        <div class='restaurant-card'>
                            <h4>🏠 {name}</h4>
                            <p><strong>⭐ மதிப்பீடு:</strong> {rating} ({count} மதிப்புரைகள்)</p>
                            <p><strong>💸 இருவருக்கான செலவு:</strong> ₹{cost}</p>
                            <p><strong>🍜 உணவுவகை:</strong> {cuisine}</p>
                            <p><strong>📍 பகுதி:</strong> {area}</p>
                        </div>
                        """, unsafe_allow_html=True)

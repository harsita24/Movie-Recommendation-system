import streamlit as st
import pandas as pd
import requests
import pickle

# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# Function to fetch movie poster
def fetch_poster(movie_id):
    api_key = '5fb00487935440179a5c5d6660f1c2e7'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=Error"

# Streamlit UI config
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Inject custom CSS
st.markdown("""
    <style>
    body {
        background-image: url("https://images.unsplash.com/photo-1600370426813-37182b50eb6f");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
    }
    .css-10trblm, .css-1v0mbdj, .css-qbe2hs, .css-1cpxqw2, .css-1d391kg {
        color: white !important;
    }
    .stButton>button {
        color: white;
        background-color: #ff4b4b;
        border: none;
        padding: 0.5em 1em;
        font-weight: bold;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #ff1f1f;
    }
    .stSelectbox label {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("🎬 Movie Recommendation System")

# Movie selection dropdown
selected_movie = st.selectbox("Select a movie:", movies['title'].values)

# Recommendation button
if st.button('Recommend'):
    st.subheader("Top 10 Recommended Movies:")
    recommendations = get_recommendations(selected_movie)

    for i in range(0, 10, 5):  # Two rows of 5 movies
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i + 5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)

                with col:
                    st.image(poster_url, width=150)
                    st.markdown(f"<h5 style='text-align: center; color: white;'>{movie_title}</h5>", unsafe_allow_html=True)

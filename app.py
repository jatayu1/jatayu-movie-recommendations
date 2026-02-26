import streamlit as st
import pickle
import requests
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OMDB_API_KEY")

movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Initialize memory for our app
if 'dismissed_movies' not in st.session_state:
    st.session_state.dismissed_movies = set()
if 'current_search' not in st.session_state:
    st.session_state.current_search = None

def omdbapi_data(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        # OMDB returns Response: "False" if movie not found
        if data.get("Response") == "False":
            return {}

        return data

    except Exception as e:
        return None

def fetch_movie_data_with_fallback(row):
    # Priority order
    titles = [
        row.get('original_title'),
        row.get('title_x'),
        row.get('title_y')
    ]

    for title in titles:
        if not title:
            continue

        data = omdbapi_data(title)

        if data and data.get("Response", "True") != "False":
            return data, title  # return which title worked

    return {}, None

def format_runtime(runtime_str):
    if not runtime_str or runtime_str == "N/A":
        return "N/A"
    
    try:
        # Extract only the numbers from strings like "132 min"
        minutes = int(''.join(filter(str.isdigit, runtime_str)))
        
        hours = minutes // 60
        leftover_minutes = minutes % 60
        
        if hours > 0:
            return f"{hours}h {leftover_minutes}m"
        else:
            return f"{leftover_minutes}m"
            
    except ValueError:
        # Fallback just in case OMDB sends something weird
        return runtime_str

# Callback function to handle the button click
def remove_movie(movie_index):
    st.session_state.dismissed_movies.add(movie_index)

def recommend(movie):
    movie_index = movies_list[movies_list['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    
    # getting valid similar movies
    valid_movies = []

    for idx, score in distances:
        if idx not in st.session_state.dismissed_movies:
            valid_movies.append((idx, score))
        if len(valid_movies) == 10:
            break
    
    if not valid_movies:
        st.info("No more recommendations available for this movie.")
        return

    with st.spinner("Curating your customized list... 🍿"):
        # Loop through chunks of 5 for our rows
        for i in range(0, len(valid_movies), 5): 
            cols = st.columns(5)
            row_movies = valid_movies[i:i+5]
            
            for col, movie_tuple in zip(cols, row_movies):
                current_idx = movie_tuple[0]
                row = movies_list.iloc[current_idx]
                movie_data, used_title = fetch_movie_data_with_fallback(row)
                
                poster = movie_data.get("Poster") if movie_data else None
                rating = movie_data.get("imdbRating") if movie_data else None
                year = movie_data.get("Year") if movie_data else None
                
                with col:
                    if poster and poster != "N/A":
                        st.image(poster, use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x450?text=No+Image", use_container_width=True)
                    
                    st.markdown(f"**{used_title}**")
                    
                    meta_text = []
                    if rating and rating != "N/A":
                        meta_text.append(f"⭐ {rating}")
                    if year and year != "N/A":
                        meta_text.append(f"📅 {year}")
                        
                    if meta_text:
                        st.caption(" | ".join(meta_text))
                        
                    # Add the dismiss button with a unique key and a callback
                    st.button("Remove", 
                              key=f"dismiss_{current_idx}", 
                              on_click=remove_movie, 
                              args=(current_idx,),
                              use_container_width=True)

st.title('Movie Recommender System')

movies_list_titles = movies_list['original_title'].values
selected_movie_name = st.selectbox("Select a movie", movies_list_titles)

# When they search, save it to session state and clear old dismissals
if st.button('Recommend'):
    st.session_state.current_search = selected_movie_name
    st.session_state.dismissed_movies.clear() 

# --- DISPLAY BLOCK ---
if 'current_search' in st.session_state and st.session_state.current_search:
    
    # 1. Get the row for the selected movie
    selected_movie_row = movies_list[movies_list['original_title'] == st.session_state.current_search].iloc[0]
    
    # 2. Fetch the rich data from your OMDB function
    movie_data, used_title = fetch_movie_data_with_fallback(selected_movie_row)
    # st.write(movie_data)
    # 3. Create a nice layout for the selected movie
    st.markdown("---")
    st.subheader("🎬 Your Selected Movie")
    
    # Make the left column smaller for the poster, right column wider for text
    info_col1, info_col2 = st.columns([1, 2.5]) 
    
    with info_col1:
        poster = movie_data.get("Poster") if movie_data else None
        if poster and poster != "N/A":
            st.image(poster, use_container_width=True)
        else:
            st.image("https://via.placeholder.com/300x450?text=No+Image", use_container_width=True)
            
    with info_col2:
        # Display the Title
        st.markdown(f"## {used_title or st.session_state.current_search}")
        
        # Display OMDB details if the API returned data
        if movie_data and movie_data.get("Response") != "False":
            st.write(f"**⭐ IMDb:** {movie_data.get('imdbRating', 'N/A')}  |  **📅 Year:** {movie_data.get('Year', 'N/A')}  |  **⏱️ Runtime:** {format_runtime(movie_data.get('Runtime', 'N/A'))}")
            st.write(f"**🎭 Genre:** {movie_data.get('Genre', 'N/A')}")
            st.write(f"**🎬 Director:** {movie_data.get('Director', 'N/A')}")
            st.write(f"**🎭 Cast:** {movie_data.get('Actors', 'N/A')}")
            st.write(f"**📖 Plot:** {movie_data.get('Plot', 'N/A')}")
            if movie_data.get("Awards"):
                st.write(f"**🏆 Awards:** {movie_data.get('Awards', 'N/A')}")
        else:
            st.warning("Could not fetch extra details from OMDB for this title.")
            
    # 4. Show the recommendations below it
    st.markdown("---")
    st.subheader("🍿 Because you liked this, we recommend:")
    recommend(st.session_state.current_search)
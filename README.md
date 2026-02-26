# Movie Recommender System (Content-Based)

This project is a content-based movie recommendation system built using Python and Streamlit.
It recommends movies similar to a selected title using cosine similarity on textual movie features.
The application is enhanced with OMDb API integration to display posters and detailed movie information such as ratings, genre, cast, and plot.

The system is interactive and allows users to remove recommendations dynamically, updating results in real time without reloading the page.

---

## Project Overview

The recommendation engine is built using content-based filtering. Movie features such as overview, genres, keywords, cast, and director are combined, vectorized, and compared using cosine similarity.

To make the system scalable and suitable for deployment, only the Top-K most similar movies per title are stored instead of a full similarity matrix. This significantly reduces memory usage while preserving recommendation quality.

Metadata enrichment is handled using the OMDb API with fallback logic to improve reliability when movie titles differ across datasets.

---

## Features

- Content-based movie recommendations  
- Top 10 similar movies per selection  
- Optimized Top-K similarity storage (memory efficient)  
- Interactive removal of unwanted recommendations  
- Session-aware recommendation logic using Streamlit session state  
- Movie posters and metadata fetched from OMDb API  
- Secure handling of API keys using environment variables  
- Fallback title matching for better API success  

---

## Installation and Setup

### 1. Clone the Repository

git clone https://github.com/jatayu1/jatayu-movie-recommendations.git
cd jatayu-movie-recommendations

### 2. Create and Activate a Virtual Environment

python -m venv venv

Windows:
venv\\Scripts\\activate

macOS / Linux:
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure OMDb API Key

Create a `.env` file in the root directory:

OMDB_API_KEY=your_omdb_api_key_here

You can obtain a free API key from: https://www.omdbapi.com/

Make sure the `.env` file is excluded from version control.

### 5. Run the Application

streamlit run app.py

The application will open in your default web browser.

---

## Data and Model Details

### movies.pkl
- A Pandas DataFrame containing movie metadata and processed features  
- Used to map movie indices to titles and display information  

### similarity_top10.pkl
- A dictionary storing the Top-10 most similar movies per movie  
- Format:
  {
    movie_index: [(similar_index, similarity_score), ...]
  }
- This replaces the full similarity matrix to reduce memory usage  

---

## Recommendation Logic

1. The selected movie index is identified from the dataset  
2. Precomputed Top-K similar movies are retrieved  
3. Previously dismissed movies are filtered out  
4. Up to 10 valid recommendations are displayed dynamically  
5. If no recommendations remain, the user is informed  

This approach ensures fast response time and scalable deployment.

---

## OMDb API Integration

To improve the success rate of metadata fetching, the system attempts multiple title variations in the following order:

- original_title  
- title_x  
- title_y  

The first successful response is used to populate the UI.

---

## Session State Management

The application uses Streamlit session state to:

- Track dismissed movies  
- Persist the current movie selection  

This allows interactive behavior without breaking the recommendation flow during reruns.

---

## Common Issues

Posters or metadata not loading:
- Verify that the OMDb API key is valid  
- Check internet connectivity  
- Some titles may not exist in OMDb  

Application fails to start:
- Ensure `movies.pkl` and `similarity_top10.pkl` are present  
- Confirm Python version is 3.8 or higher  

---

## Technology Stack

- Python  
- Streamlit  
- Pandas and NumPy  
- Scikit-learn  
- OMDb API  
- python-dotenv  

---

## Future Improvements

- Search-based movie selection  
- Genre and year filters  
- Hybrid recommendation approach  
- User profiles and recommendation history  
- Analytics dashboard for movie insights  

---

## Author

Akash Das  
Data Scientist and Full-Stack Developer  
Portfolio: akashdascodes.com  

---

## License

This project is licensed under the MIT License.

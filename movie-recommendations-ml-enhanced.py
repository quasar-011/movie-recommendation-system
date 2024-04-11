# Import the required libraries
from sklearn.model_selection import train_test_split
from surprise import Dataset, Reader, SVD
from fuzzywuzzy import process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from joblib import dump, load

# Load the Datasets
ratings_data = pd.read_csv('/home/quasar_011/Developer/datasets/movieLens/rating.csv')
movies_data = pd.read_csv('/home/quasar_011/Developer/datasets/movieLens/movie.csv')
tags_data = pd.read_csv('/home/quasar_011/Developer/datasets/movieLens/tag.csv')

# Split the dataset
train_data, test_data = train_test_split(ratings_data, test_size=0.2, random_state=42)

# Training
reader = Reader(rating_scale=(1, 5))
train_dataset = Dataset.load_from_df(train_data[['userId', 'movieId', 'rating']], reader)
model = SVD()
trainset = train_dataset.build_full_trainset()
model.fit(trainset)

# Save the model
dump(model, 'SVD_model.joblib')

# Load the model
loaded_model = load('SVD_model.joblib'

# User input function
def get_user_input():
    selected_movies = []
    selected_genres = []
    
    print("Enter a movie title (or press Enter to stop adding movies):")
    while True:
        movie_title = input().strip()
        if not movie_title:
            break
        selected_movies.append(movie_title)
        if len(selected_movies) >= 4:
            print("You have reached the maximum number of movies (4).")
            break
    
    print("Enter a genre (or press Enter to stop adding genres):")
    while True:
        genre = input().strip()
        if not genre:
            break
        selected_genres.append(genre)
    
    return selected_movies, selected_genres

# Similar movie function
def get_similar_movies(selected_movies, selected_genres):
    similar_movies = []
    for movie_title in selected_movies:
        # Match the closest movieName string 
        match = process.extractOne(movie_title, movies_data['title'])
        matched_movie_title = match[0]

        # Get the movieId of the matched movie
        matched_movie_id = movies_data.loc[movies_data['title'] == matched_movie_title, 'movieId'].values[0]

        # Get movie genres
        movie_genres = movies_data.loc[movies_data['title'] == matched_movie_title, 'genres'].values[0]

        # Calculate TF-IDF vectors for movie genres
        tfidf = TfidfVectorizer(stop_words='english')
        genres_tfidf_matrix = tfidf.fit_transform(movies_data['genres'])

        # Calculate TF-IDF vector for input genres
        input_genres_tfidf = tfidf.transform([','.join(selected_genres)])

        # Calculate cosine similarity between input genres and all movies
        cosine_similarities = linear_kernel(input_genres_tfidf, genres_tfidf_matrix).flatten()

        # Get indices of top similar movies based on genres
        similar_movie_indices = cosine_similarities.argsort()[::-1]

        # Filter out the input movie and select top 10 similar movies
        similar_movie_indices = similar_movie_indices[similar_movie_indices != matched_movie_id][:10]

        # Get movie titles and genres of similar movies
        similar_movies_info = movies_data.iloc[similar_movie_indices][['title', 'genres']].values.tolist()

        # Add similar movies to the list
        similar_movies.extend(similar_movies_info)
        
    # Return only top 10 similar movies
    return similar_movies[:10]

# Get user input
selected_movies, selected_genres = get_user_input()

# Get similar movies based on user input
similar_movies = get_similar_movies(selected_movies, selected_genres)

# Display similar movies
print("\nSimilar movies based on selected movies and genres:")
print("Top 10 recommendations:")
for idx, movie in enumerate(similar_movies, start=1):
    print(f"     {idx}: MovieName: {movie[0]}, \t Genres: {movie[1]}")

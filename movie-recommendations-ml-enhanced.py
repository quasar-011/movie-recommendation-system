
import pandas as pd
from sklearn.model_selection import train_test_split
from surprise import Dataset, Reader, SVD
from fuzzywuzzy import process

# Load datasets
ratings_data = pd.read_csv('/home/quasar_011/Developer/datasets/movieLens/rating.csv')
movies_data = pd.read_csv('/home/quasar_011/Developer/datasets/movieLens/movie.csv')
tags_data = pd.read_csv('/home/quasar_011/Developer/datasets/movieLens/tag.csv')

# Train-test split
train_data, test_data = train_test_split(ratings_data, test_size=0.2, random_state=42)

# Train the SVD model
reader = Reader(rating_scale=(1, 5))
train_dataset = Dataset.load_from_df(train_data[['userId', 'movieId', 'rating']], reader)
model = SVD()
trainset = train_dataset.build_full_trainset()
model.fit(trainset)

# Function to get user input for movies and genres
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

# Function to get similar movies based on user input
def get_similar_movies(selected_movies, selected_genres):
    similar_movies = []
    for movie_title in selected_movies:
        match = process.extractOne(movie_title, movies_data['title'])
        matched_movie_title = match[0]
        
        # Find similar movies based on genres
        similar_movie_ids = movies_data[movies_data['genres'].apply(lambda x: any(genre in x for genre in movies_data[movies_data['title'] == matched_movie_title]['genres'].values[0]))]
        
        # Exclude the input movie from similar movies
        similar_movie_ids = similar_movie_ids[similar_movie_ids['title'] != matched_movie_title]
        
        # Sample similar movies if there are more than 10
        if len(similar_movie_ids) > 10:
            similar_movie_ids = similar_movie_ids.sample(n=10, replace=False, random_state=42)
        
        # Add similar movies to the list
        similar_movies.extend(similar_movie_ids[['title', 'genres']].values.tolist())
    
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
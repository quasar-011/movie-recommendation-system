<h1>Movie Recommendation System using Machine Learning in Python</h1> 
<hr>
<h2>Overview</h2>
This project implements a Movie Recommendation System using Singular Value Decomposition (SVD) on the MovieLens dataset. The system suggests personalized movie recommendations based on user ratings and movie features.

<h2>Dataset</h2>
The MovieLens dataset is used as the foundation for this recommendation system. It contains movie ratings provided by users as well as movie metadata such as titles and genres.You can download it from this link : https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset

<h2> Methodology </h2>
    Data Preprocessing: The dataset present is clean and does not need to be preprocessed to be executed. Thus, you can skip this step.
    Singular Value Decomposition (SVD): SVD is applied to the user-item rating matrix to decompose it into lower-dimensional matrices, capturing latent factors.
    Model Training: The SVD model is trained on the processed data to learn user preferences and movie features.
    Recommendation Generation: Based on the trained model, recommendations are generated for users by predicting ratings for unrated movies.
    Evaluation: The performance of the recommendation system is evaluated using metrics such as accuracy, precision, and recall.

<h2> Usage </h2>
    Setup: Clone the repository and install necessary dependencies.
    Data Preparation: Download the MovieLens dataset from the given link and convert the files from tsv to csv.
    Model Training: Train the SVD model on the preprocessed dataset.
    Recommendation Generation: Input user preferences (movies liked, genres preferred) and generate personalized recommendations.
    Evaluation: Evaluate the performance of the recommendation system using appropriate metrics.

<h2>Requirements</h2>
    Python 3.x
    Pandas
    NumPy
    Surprise
    scikit-learn

<h2> Reference </h2>
MovieLens:[Link](https://movielens.org/)

<h2>License</h2> 
This project is licensed under the MIT License. See the [License](https://github.com/quasar-011/movie-recommendation-system/blob/main/LICENSE) file for details.

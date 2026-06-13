import pandas as pd
import pickle
import os

# Chemin absolu vers backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data = {
    "title": [
        "The Dark Knight", "Inception", "Interstellar", "The Matrix",
        "Avengers Endgame", "Iron Man", "Spider-Man", "Black Panther",
        "The Godfather", "Pulp Fiction", "Fight Club", "Forrest Gump",
        "The Shawshank Redemption", "Titanic", "Avatar",
        "Joker", "Batman Begins", "The Dark Knight Rises",
        "Doctor Strange", "Thor"
    ],
    "genres": [
        "action crime thriller", "action scifi thriller", "scifi drama adventure",
        "action scifi", "action adventure scifi", "action adventure scifi",
        "action adventure", "action adventure scifi", "crime drama",
        "crime thriller drama", "thriller drama", "drama romance",
        "drama", "romance drama", "scifi adventure",
        "crime thriller drama", "action crime thriller", "action crime thriller",
        "action scifi fantasy", "action adventure fantasy"
    ],
    "poster": [
    "https://placehold.co/300x450/1a1a2e/FFD700?text=The+Dark+Knight",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Inception",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Interstellar",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=The+Matrix",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Avengers+Endgame",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Iron+Man",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Spider-Man",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Black+Panther",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=The+Godfather",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Pulp+Fiction",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Fight+Club",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Forrest+Gump",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Shawshank",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Titanic",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Avatar",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Joker",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Batman+Begins",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Dark+Knight+Rises",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Doctor+Strange",
    "https://placehold.co/300x450/1a1a2e/FFD700?text=Thor",
]
}

df = pd.DataFrame(data)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df["genres"])

pickle.dump(df, open(os.path.join(BASE_DIR, "movies.pkl"), "wb"))
pickle.dump(tfidf_matrix, open(os.path.join(BASE_DIR, "features.pkl"), "wb"))
print("Dataset créé avec", len(df), "films")
import os
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies = pickle.load(open(os.path.join(BASE_DIR, "movies.pkl"), "rb"))
tfidf_matrix = pickle.load(open(os.path.join(BASE_DIR, "features.pkl"), "rb"))

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend(movie_index):
    scores = list(enumerate(cosine_sim[movie_index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    result = []
    for i in scores:
        row = movies.iloc[i[0]]
        result.append({
            "title": row["title"],
            "genre": row["genres"],
            "poster": row["poster"]
        })
    return result

def recommend_by_name(title):
    title = title.lower()
    matches = movies[movies["title"].str.lower() == title]
    if matches.empty:
        matches = movies[movies["title"].str.lower().str.contains(title)]
    if matches.empty:
        return []
    index = matches.index[0]
    return recommend(index)
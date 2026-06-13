import torch
import torch.nn as nn
from torch_geometric.nn import LGConv
import pickle
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(BASE_DIR)

# Chargement des données sauvegardées
data = pickle.load(open(os.path.join(BACKEND_DIR, "lightgcn_data.pkl"), "rb"))
movies = pd.read_csv(os.path.join(BACKEND_DIR, "ml-latest-small/movies.csv"))

n_users = data['n_users']
n_movies = data['n_movies']
movie_ids = data['movie_ids']
movie_idx_to_id = data['movie_idx_to_id']
train_edge_index = data['train_edge_index']

class LightGCN(nn.Module):
    def __init__(self, n_users, n_items, emb_dim=128, n_layers=4):
        super().__init__()
        self.n_users = n_users
        self.n_items = n_items
        self.embedding = nn.Embedding(n_users + n_items, emb_dim)
        self.convs = nn.ModuleList([LGConv() for _ in range(n_layers)])

    def forward(self, edge_index):
        x = self.embedding.weight
        embeddings = [x]
        for conv in self.convs:
            x = conv(x, edge_index)
            embeddings.append(x)
        final = torch.stack(embeddings, dim=1).mean(dim=1)
        return final[:self.n_users], final[self.n_users:]

# Chargement du modèle
device = torch.device('cpu')
model = LightGCN(n_users, n_movies).to(device)
model.load_state_dict(torch.load(
    os.path.join(BACKEND_DIR, "lightgcn_model.pt"),
    map_location=device
))
model.eval()

# Pré-calcul des embeddings
with torch.no_grad():
    user_emb, item_emb = model(train_edge_index)

def recommend_by_user(user_idx, top_k=10):
    with torch.no_grad():
        scores = torch.matmul(user_emb[user_idx], item_emb.T)
        top_items = scores.argsort(descending=True)[:top_k].numpy()
    result = []
    for idx in top_items:
        movie_id = movie_idx_to_id[int(idx)]
        row = movies[movies['movieId'] == movie_id].iloc[0]
        result.append({
            "title": row['title'],
            "genre": row['genres'],
            "poster": f"https://placehold.co/300x450/1a1a2e/FFD700?text={row['title'][:15].replace(' ', '+')}"
        })
    return result

def recommend_by_title(title, top_k=10):
    title_lower = title.lower()
    match = movies[movies['title'].str.lower().str.contains(title_lower)]
    if match.empty:
        return []
    movie_id = match.iloc[0]['movieId']
    if movie_id not in movie_ids:
        return []
    movie_idx = movie_ids[movie_id]
    with torch.no_grad():
        scores = torch.matmul(item_emb[movie_idx], item_emb.T)
        top_items = scores.argsort(descending=True)[1:top_k+1].numpy()
    result = []
    for idx in top_items:
        mid = movie_idx_to_id[int(idx)]
        row = movies[movies['movieId'] == mid].iloc[0]
        result.append({
            "title": row['title'],
            "genre": row['genres'],
            "poster": f"https://placehold.co/300x450/1a1a2e/FFD700?text={row['title'][:15].replace(' ', '+')}"
        })
    return result
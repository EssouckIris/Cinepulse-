import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from torch_geometric.nn import LGConv
from sklearn.model_selection import train_test_split
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "ml-latest-small")

# 1. DONNÉES
ratings = pd.read_csv(f"{DATA_DIR}/ratings.csv")
movies = pd.read_csv(f"{DATA_DIR}/movies.csv")

user_ids = {v: i for i, v in enumerate(ratings['userId'].unique())}
movie_ids = {v: i for i, v in enumerate(ratings['movieId'].unique())}
movie_idx_to_id = {v: k for k, v in movie_ids.items()}

ratings['user_idx'] = ratings['userId'].map(user_ids)
ratings['movie_idx'] = ratings['movieId'].map(movie_ids)

n_users = len(user_ids)
n_movies = len(movie_ids)

train_df, test_df = train_test_split(ratings, test_size=0.2, random_state=42)

# 2. GRAPHE
def build_edge_index(df, n_users):
    users = torch.tensor(df['user_idx'].values, dtype=torch.long)
    items = torch.tensor(df['movie_idx'].values + n_users, dtype=torch.long)
    edge_index = torch.stack([
        torch.cat([users, items]),
        torch.cat([items, users])
    ])
    return edge_index

train_edge_index = build_edge_index(train_df, n_users)

# 3. MODÈLE
class LightGCN(nn.Module):
    def __init__(self, n_users, n_items, emb_dim=128, n_layers=4):
        super().__init__()
        self.n_users = n_users
        self.n_items = n_items
        self.n_layers = n_layers
        self.embedding = nn.Embedding(n_users + n_items, emb_dim)
        nn.init.xavier_uniform_(self.embedding.weight)
        self.convs = nn.ModuleList([LGConv() for _ in range(n_layers)])

    def forward(self, edge_index):
        x = self.embedding.weight
        embeddings = [x]
        for conv in self.convs:
            x = conv(x, edge_index)
            embeddings.append(x)
        final = torch.stack(embeddings, dim=1).mean(dim=1)
        return final[:self.n_users], final[self.n_users:]

def bpr_loss(user_emb, pos_emb, neg_emb):
    pos_scores = (user_emb * pos_emb).sum(dim=1)
    neg_scores = (user_emb * neg_emb).sum(dim=1)
    return -torch.log(torch.sigmoid(pos_scores - neg_scores)).mean()

# 4. ENTRAÎNEMENT
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = LightGCN(n_users, n_movies, emb_dim=128, n_layers=4).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
train_edge_index = train_edge_index.to(device)

train_users = torch.tensor(train_df['user_idx'].values, dtype=torch.long)
train_movies_t = torch.tensor(train_df['movie_idx'].values, dtype=torch.long)

print("Entraînement LightGCN amélioré...")
# 4. ENTRAÎNEMENT AVEC COURBE DE LOSS
import matplotlib.pyplot as plt

losses = []

print("Entraînement LightGCN...")
for epoch in range(50):
    model.train()
    optimizer.zero_grad()
    user_emb, item_emb = model(train_edge_index)
    neg_movies = torch.randint(0, n_movies, (len(train_users),))
    u = user_emb[train_users.to(device)]
    pos = item_emb[train_movies_t.to(device)]
    neg = item_emb[neg_movies.to(device)]
    loss = bpr_loss(u, pos, neg)
    loss.backward()
    optimizer.step()
    losses.append(loss.item())
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}/50 — Loss: {loss.item():.4f}")

# Plot courbe de loss
plt.figure(figsize=(10, 5))
plt.style.use('dark_background')
plt.plot(range(1, 51), losses, color='#FFD700', linewidth=2)
plt.title('Courbe de Loss BPR — LightGCN', fontsize=14, fontweight='bold')
plt.xlabel('Epoch')
plt.ylabel('Loss BPR')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('loss_curve.png', dpi=150, bbox_inches='tight')
plt.show()
print("Courbe sauvegardée : loss_curve.png")
# 5. ÉVALUATION
def recall_at_k(recommended, relevant):
    if len(relevant) == 0: return 0
    return len(set(recommended) & set(relevant)) / len(relevant)

def ndcg_at_k(recommended, relevant):
    dcg = sum(1/np.log2(i+2) for i, r in enumerate(recommended) if r in relevant)
    idcg = sum(1/np.log2(i+2) for i in range(min(len(relevant), len(recommended))))
    return dcg/idcg if idcg > 0 else 0

model.eval()
with torch.no_grad():
    user_emb, item_emb = model(train_edge_index)

test_users_list = test_df['user_idx'].unique()[:100]
recalls, ndcgs = [], []
for u in test_users_list:
    relevant = test_df[test_df['user_idx'] == u]['movie_idx'].values
    scores = torch.matmul(user_emb[u], item_emb.T)
    recommended = scores.argsort(descending=True)[:10].cpu().numpy()
    recalls.append(recall_at_k(recommended, relevant))
    ndcgs.append(ndcg_at_k(recommended, relevant))

print(f"\n=== RÉSULTATS ===")
print(f"Recall@10 : {np.mean(recalls):.4f}")
print(f"NDCG@10   : {np.mean(ndcgs):.4f}")

# 6. SAUVEGARDE DU MODÈLE
torch.save(model.state_dict(), os.path.join(BASE_DIR, "lightgcn_model.pt"))
pickle.dump({
    'user_ids': user_ids,
    'movie_ids': movie_ids,
    'movie_idx_to_id': movie_idx_to_id,
    'n_users': n_users,
    'n_movies': n_movies,
    'train_edge_index': train_edge_index.cpu()
}, open(os.path.join(BASE_DIR, "lightgcn_data.pkl"), "wb"))
print("\nModèle sauvegardé !")

# 7. EXEMPLE
print("\n=== TOP 5 POUR UTILISATEUR 0 ===")
scores = torch.matmul(user_emb[0], item_emb.T)
top5 = scores.argsort(descending=True)[:5].cpu().numpy()
for r in top5:
    movie_id = movie_idx_to_id[r]
    title = movies[movies['movieId'] == movie_id]['title'].values[0]
    print(f"  - {title}")
    # ============================================================
# 10. VISUALISATION DES EMBEDDINGS AVEC t-SNE
# ============================================================
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

print("\nVisualisation des embeddings...")

# Prendre un échantillon
n_sample_users = 100
n_sample_movies = 200

user_sample = user_emb[:n_sample_users].detach().cpu().numpy()
item_sample = item_emb[:n_sample_movies].detach().cpu().numpy()

# Combiner pour t-SNE
combined = np.vstack([user_sample, item_sample])
labels = ['Utilisateur'] * n_sample_users + ['Film'] * n_sample_movies

# t-SNE
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
reduced = tsne.fit_transform(combined)

# Plot
plt.figure(figsize=(12, 8))
plt.style.use('dark_background')

colors = ['#FF00FF' if l == 'Utilisateur' else '#FFD700' for l in labels]
plt.scatter(reduced[:, 0], reduced[:, 1], c=colors, alpha=0.7, s=30)

patch1 = mpatches.Patch(color='#FF00FF', label='Utilisateurs')
patch2 = mpatches.Patch(color='#FFD700', label='Films')
plt.legend(handles=[patch1, patch2], fontsize=12)

plt.title('Visualisation t-SNE des Embeddings LightGCN', fontsize=14, fontweight='bold')
plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.tight_layout()
plt.savefig('embeddings_tsne.png', dpi=150, bbox_inches='tight')
plt.show()
print("Graphique sauvegardé : embeddings_tsne.png")
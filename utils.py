import faiss
import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np

# Paths
VECTORSTORE_DIR = "vectorstore"
INDEX_PATH = os.path.join(VECTORSTORE_DIR, "index.faiss")
META_PATH = os.path.join(VECTORSTORE_DIR, "metadata.json")

# Load model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL)

# Load FAISS index and metadata
def load_index_and_metadata():
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(f"FAISS index not found at {INDEX_PATH}")
    if not os.path.exists(META_PATH):
        raise FileNotFoundError(f"Metadata JSON not found at {META_PATH}")

    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata

# Embed a query
def embed_query(query: str):
    return model.encode([query])[0]

# Search the FAISS index and return top-k results
def search_index(query: str, top_k: int = 5):
    index, metadata = load_index_and_metadata()
    query_vector = embed_query(query).reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(metadata):
            result = metadata[idx]
            result["score"] = float(dist)
            results.append(result)
    return results

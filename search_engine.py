import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SemanticSearch:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.texts = []
        self.urls = []

    def load_data(self):
        with open("discourse_data.json") as f:
            data1 = json.load(f)
        with open("tds_content.json") as f:
            data2 = json.load(f)

        all_data = data1 + data2
        self.texts = [d['content'] for d in all_data]
        self.urls = [d.get("url", "") for d in all_data]

        self.embeddings = self.model.encode(self.texts)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings).astype("float32"))

    def query(self, question):
        q_embed = self.model.encode([question])
        D, I = self.index.search(np.array(q_embed).astype("float32"), 5)
        return [(self.texts[i], self.urls[i]) for i in I[0]]

import json
import os
from tqdm import tqdm
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import faiss
import pickle

load_dotenv()

# === Paths ===
DATA_FILES = ['discourse_data.json', 'tds_content.json']
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
VECTOR_DIR = 'vectorstore'
DB_FILE = os.path.join(VECTOR_DIR, 'index.faiss')
PKL_FILE = os.path.join(VECTOR_DIR, 'metadata.pkl')
JSON_FILE = os.path.join(VECTOR_DIR, 'metadata.json')

# === Ensure directory exists ===
os.makedirs(VECTOR_DIR, exist_ok=True)

# === Load model ===
model = SentenceTransformer(EMBEDDING_MODEL)

# === Load and chunk data ===
def load_and_chunk():
    all_chunks = []
    metadata = []
    for file in DATA_FILES:
        with open(file, 'r', encoding='utf-8') as f:
            items = json.load(f)
            for item in items:
                text = item.get("content") or item.get("text") or ""
                chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                all_chunks.extend(chunks)
                metadata.extend([item] * len(chunks))
    return all_chunks, metadata

# === Embed and store ===
def embed_and_store():
    chunks, metadata = load_and_chunk()
    print(f"Embedding {len(chunks)} chunks...")

    embeddings = model.encode(chunks, show_progress_bar=True)

    # Save FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, DB_FILE)

    # Save metadata.pkl
    with open(PKL_FILE, 'wb') as f:
        pickle.dump(metadata, f)

    # Save metadata.json (cleaning non-serializable entries)
    cleaned_metadata = []
    for item in metadata:
        cleaned_item = {
            k: str(v) if not isinstance(v, (str, int, float, bool, list, dict, type(None))) else v
            for k, v in item.items()
        }
        cleaned_metadata.append(cleaned_item)

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned_metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ Embedding complete and saved to '{VECTOR_DIR}/'.")

# === Main ===
if __name__ == "__main__":
    embed_and_store()

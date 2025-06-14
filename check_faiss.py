import os
import json
import faiss

VECTORSTORE_DIR = "vectorstore"
INDEX_FILE = os.path.join(VECTORSTORE_DIR, "index.faiss")
METADATA_JSON = os.path.join(VECTORSTORE_DIR, "metadata.json")

print("Checking FAISS and metadata files...\n")

# Check FAISS index
if os.path.exists(INDEX_FILE):
    print(f"✅ FAISS index found at: {os.path.abspath(INDEX_FILE)}")
    index = faiss.read_index(INDEX_FILE)
    print(f" - Number of vectors in index: {index.ntotal}")
    print(f" - Vector dimension: {index.d}")
else:
    print("❌ FAISS index file not found.")

# Check metadata.json
if os.path.exists(METADATA_JSON):
    print(f"✅ Metadata JSON found at: {os.path.abspath(METADATA_JSON)}")
    with open(METADATA_JSON, "r", encoding="utf-8") as f:
        metadata = json.load(f)
        print(f" - Metadata items: {len(metadata)}")
else:
    print("❌ Metadata JSON file not found.")

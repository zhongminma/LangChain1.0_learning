from pathlib import Path
import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = Path(__file__).resolve().parent
PERSIST_DIR = str(BASE_DIR / "chroma_db")
COLLECTION = "rag_demo"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def search(query: str, k: int = 4):
    print("PERSIST_DIR =", PERSIST_DIR)
    print("Exists?     =", os.path.exists(PERSIST_DIR))

    db = Chroma(
        persist_directory=PERSIST_DIR,
        collection_name=COLLECTION,
        embedding_function=embeddings,
    )

    results = db.similarity_search(query, k=k)
    print("Hits =", len(results))

    for i, d in enumerate(results, 1):
        src = d.metadata.get("source", "unknown")
        print(f"\n--- #{i} source={src} ---")
        print(d.page_content[:400])

if __name__ == "__main__":
    search("What are common side effects of aspirin.txt?", k=4)

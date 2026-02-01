from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "aspirin.txt"
STORAGE_DIR = BASE_DIR / "storage"
CHROMA_DIR = STORAGE_DIR / "chroma_db"
CHUNKS_FILE = STORAGE_DIR / "chunks.jsonl"

COLLECTION = "aspirin_demo"

# Chunking
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80

# Retrieval
BM25_K = 8
DENSE_K = 8
FINAL_TOP_K = 4

# Fusion weights (dense usually stronger for semantic)
W_BM25 = 0.4
W_DENSE = 0.6

# Embedding model
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Reranker model (Cross-Encoder)
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

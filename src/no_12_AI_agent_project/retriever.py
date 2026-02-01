import json
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Tuple

from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from sentence_transformers import CrossEncoder

from config import (
    CHROMA_DIR,
    CHUNKS_FILE,
    COLLECTION,
    BM25_K,
    DENSE_K,
    FINAL_TOP_K,
    W_BM25,
    W_DENSE,
    EMBED_MODEL,
    RERANK_MODEL,
)


# ---------- IO ----------
def load_docs_from_jsonl() -> List[Document]:
    """Load chunked documents from storage/chunks.jsonl."""
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Missing chunks file: {CHUNKS_FILE}. Run ingest.py first."
        )

    docs: List[Document] = []
    with CHUNKS_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            docs.append(
                Document(
                    page_content=obj["text"],
                    metadata=obj.get("metadata", {}),
                )
            )
    if not docs:
        raise RuntimeError(f"No docs loaded from {CHUNKS_FILE}. File is empty?")
    return docs


# ---------- Utils ----------
def _dedupe_key(d: Document) -> Tuple:
    """Stable key used for de-duplication across bm25 + dense results."""
    md = d.metadata or {}
    # chunk_id is the most stable; fall back to content prefix
    return (md.get("source"), md.get("chunk_id"), d.page_content[:80])


def format_context(docs: List[Document]) -> str:
    """Format docs into a numbered context block."""
    parts = []
    for i, d in enumerate(docs, 1):
        md = d.metadata or {}
        parts.append(
            f"[{i}] source={md.get('source')} chunk_id={md.get('chunk_id')}\n{d.page_content}"
        )
    return "\n\n".join(parts)


# ---------- Hybrid Recall ----------
def hybrid_recall(query: str, docs: List[Document]) -> Tuple[List[Document], Dict]:
    """
    Hybrid recall:
      - sparse: BM25
      - dense: Chroma similarity search
      - fusion: weighted rank-based merge
    Returns: (merged_candidates, debug_dict)
    """
    # 1) sparse BM25
    bm25 = BM25Retriever.from_documents(docs)
    bm25.k = BM25_K
    bm25_hits = bm25.invoke(query)

    # 2) dense Chroma
    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            f"Missing chroma dir: {CHROMA_DIR}. Run ingest.py first."
        )

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = Chroma(
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION,
        embedding_function=embeddings,
    )
    dense_hits = vs.similarity_search(query, k=DENSE_K)

    # 3) fusion merge (rank-based weighted)
    scores = defaultdict(float)
    pool: Dict[Tuple, Document] = {}

    bm25_ids = []
    dense_ids = []

    for rank, d in enumerate(bm25_hits, 1):
        k = _dedupe_key(d)
        scores[k] += W_BM25 * (1.0 / rank)
        pool[k] = d
        bm25_ids.append(d.metadata.get("chunk_id"))

    for rank, d in enumerate(dense_hits, 1):
        k = _dedupe_key(d)
        scores[k] += W_DENSE * (1.0 / rank)
        pool[k] = d
        dense_ids.append(d.metadata.get("chunk_id"))

    merged_keys = sorted(pool.keys(), key=lambda k: scores[k], reverse=True)
    merged = [pool[k] for k in merged_keys]

    debug = {
        "bm25_top_chunk_ids": bm25_ids,
        "dense_top_chunk_ids": dense_ids,
        "fusion_top_chunk_ids": [d.metadata.get("chunk_id") for d in merged[:12]],
        "weights": {"bm25": W_BM25, "dense": W_DENSE},
        "k": {"bm25": BM25_K, "dense": DENSE_K},
        "collection": COLLECTION,
    }
    return merged, debug


# ---------- Rerank ----------
def rerank(query: str, candidates: List[Document]) -> Tuple[List[Document], Dict]:
    """
    Cross-encoder rerank over candidates.
    Returns: (top_docs, debug_dict)
    """
    if not candidates:
        return [], {"rerank_model": RERANK_MODEL, "rerank_scores": [], "rerank_top_chunk_ids": []}

    ce = CrossEncoder(RERANK_MODEL)

    pairs = [(query, d.page_content) for d in candidates]
    scores = ce.predict(pairs)

    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    top = [d for d, _ in ranked[:FINAL_TOP_K]]
    top_scores = [float(s) for _, s in ranked[:FINAL_TOP_K]]
    top_ids = [d.metadata.get("chunk_id") for d in top]

    debug = {
        "rerank_model": RERANK_MODEL,
        "rerank_scores": top_scores,
        "rerank_top_chunk_ids": top_ids,
        "final_top_k": FINAL_TOP_K,
    }
    return top, debug


# ---------- Public APIs ----------
def retrieve(query: str) -> List[Document]:
    """Retrieve top docs using hybrid recall + rerank."""
    docs = load_docs_from_jsonl()
    candidates, _rec_debug = hybrid_recall(query, docs)
    top, _rer_debug = rerank(query, candidates)
    return top


def retrieve_with_debug(query: str) -> Tuple[List[Document], Dict]:
    """
    Retrieve and also return a structured debug payload suitable for logging to JSONL.
    """
    docs = load_docs_from_jsonl()
    candidates, rec_debug = hybrid_recall(query, docs)
    top, rer_debug = rerank(query, candidates)

    debug = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "recall": {
            "method": "bm25+dense",
            "bm25_top_chunk_ids": rec_debug["bm25_top_chunk_ids"],
            "dense_top_chunk_ids": rec_debug["dense_top_chunk_ids"],
            "fusion_top_chunk_ids": rec_debug["fusion_top_chunk_ids"],
            "weights": rec_debug["weights"],
            "k": rec_debug["k"],
            "collection": rec_debug["collection"],
        },
        "rerank": rer_debug,
        "final_k": FINAL_TOP_K,
    }
    return top, debug


# ---------- Quick manual test ----------
if __name__ == "__main__":
    q = "Why should aspirin be avoided in children and what is the bleeding risk?"
    docs, debug = retrieve_with_debug(q)
    print(json.dumps(debug, indent=2))
    print("\n--- CONTEXT ---\n")
    print(format_context(docs))

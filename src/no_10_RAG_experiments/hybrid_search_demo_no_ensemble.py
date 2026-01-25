from pathlib import Path
from collections import defaultdict

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever


BASE = Path(__file__).resolve().parent
DATA_FILE = BASE / "data" / "aspirin.txt"
PERSIST_DIR = BASE / "chroma_db"
COLLECTION = "rag_demo"


def build_docs():
    text = DATA_FILE.read_text(encoding="utf-8")
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=80)
    chunks = splitter.split_text(text)
    return [Document(page_content=c, metadata={"source": "aspirin.txt", "chunk": i}) for i, c in enumerate(chunks)]


def hybrid_search(query: str, docs, vectorstore, *, k_bm25=4, k_dense=4, w_bm25=0.5, w_dense=0.5):
    # 1) sparse: BM25
    bm25 = BM25Retriever.from_documents(docs)
    bm25.k = k_bm25
    bm25_hits = bm25.invoke(query)

    # 2) dense: Vector
    dense_hits = vectorstore.similarity_search(query, k=k_dense)

    # 3) merge + simple scoring (rank-based)
    scores = defaultdict(float)
    by_key = {}

    def key(d: Document):
        # 用 (source, chunk) 当唯一键；没有的话退化用内容
        return (d.metadata.get("source"), d.metadata.get("chunk"), d.page_content[:60])

    for rank, d in enumerate(bm25_hits, 1):
        scores[key(d)] += w_bm25 * (1.0 / rank)
        by_key[key(d)] = d

    for rank, d in enumerate(dense_hits, 1):
        scores[key(d)] += w_dense * (1.0 / rank)
        by_key[key(d)] = d

    merged = sorted(by_key.keys(), key=lambda k: scores[k], reverse=True)
    return [by_key[k] for k in merged]


if __name__ == "__main__":
    docs = build_docs()

    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vs = Chroma.from_documents(
        docs,
        embedding=emb,
        persist_directory=str(PERSIST_DIR),
        collection_name=COLLECTION,
    )

    q = "aspirin bleeding risk and blood thinners"
    results = hybrid_search(q, docs, vs, k_bm25=4, k_dense=4, w_bm25=0.4, w_dense=0.6)

    print(f"Query: {q}\nHits: {len(results)}")
    for i, d in enumerate(results, 1):
        print(f"\n--- #{i} meta={d.metadata} ---")
        print(d.page_content[:350])

from dotenv import load_dotenv
load_dotenv()

from rag.config import RAGConfig
from rag.loaders import load_raw_texts
from rag.chunking import split_docs
from rag.embeddings import build_embeddings
from rag.vectorstore import build_vectorstore, upsert_documents

def main():
    cfg = RAGConfig()
    docs = load_raw_texts(cfg.raw_dir)
    if not docs:
        raise RuntimeError(f"No documents found in: {cfg.raw_dir}")

    chunks = split_docs(docs, cfg.chunk_size, cfg.chunk_overlap)
    embeddings = build_embeddings(cfg.embed_model)

    vs = build_vectorstore(
        persist_dir=str(cfg.chroma_dir),
        collection_name="rag_demo",
        embedding_fn=embeddings,
    )

    n = upsert_documents(vs, chunks)
    print(f"✅ Ingest done. Raw docs={len(docs)}, chunks={len(chunks)}, inserted={n}")
    print(f"📦 Chroma persisted at: {cfg.chroma_dir}")

if __name__ == "__main__":
    main()

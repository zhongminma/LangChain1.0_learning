from dotenv import load_dotenv
load_dotenv()

from rag.config import RAGConfig
from rag.embeddings import build_embeddings
from rag.vectorstore import build_vectorstore, get_retriever
from rag.pipeline import build_rag_chain

def main():
    cfg = RAGConfig()

    embeddings = build_embeddings(cfg.embed_model)
    vs = build_vectorstore(
        persist_dir=str(cfg.chroma_dir),
        collection_name="rag_demo",
        embedding_fn=embeddings,
    )

    retriever = get_retriever(vs, cfg.k)
    chain = build_rag_chain(cfg.chat_model, retriever)

    print("🤖 RAG Chat ready. Type your question (Ctrl+C to exit).")
    while True:
        q = input("\nYou: ").strip()
        if not q:
            continue
        ans = chain.invoke(q)
        print("\nAssistant:", ans)

if __name__ == "__main__":
    main()

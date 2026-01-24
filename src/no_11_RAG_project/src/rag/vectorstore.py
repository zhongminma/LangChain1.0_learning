from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

def build_vectorstore(persist_dir: str, collection_name: str, embedding_fn):
    return Chroma(
        collection_name=collection_name,
        embedding_function=embedding_fn,
        persist_directory=persist_dir,
    )

def upsert_documents(vs: Chroma, docs: List[Document]) -> int:
    ids = vs.add_documents(docs)
    vs.persist()
    return len(ids)

def get_retriever(vs: Chroma, k: int):
    return vs.as_retriever(search_kwargs={"k": k})

import re
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- stable paths (relative to this script) ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PERSIST_DIR = BASE_DIR / "chroma_db"
COLLECTION = "rag_demo"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def preprocess_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_docs():
    print("DATA_DIR =", str(DATA_DIR))
    print("Files   =", [str(p) for p in DATA_DIR.rglob("*.*")][:10])

    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.txt",                 # 先只扫 txt，最稳
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
        use_multithreading=True,
        silent_errors=False,             # 先别吞错
    )
    return loader.load()


def build_index():
    docs = load_docs()
    if not docs:
        raise RuntimeError(f"No documents found under {DATA_DIR}. Put some .txt files there.")

    for d in docs:
        d.page_content = preprocess_text(d.page_content)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    print(f"Loaded docs: {len(docs)} | Chunks: {len(chunks)}")

    PERSIST_DIR.mkdir(parents=True, exist_ok=True)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION,
        persist_directory=str(PERSIST_DIR),
    )
    # vectordb.persist()
    print(f"✅ Index built & persisted to: {PERSIST_DIR} (collection={COLLECTION})")


if __name__ == "__main__":
    build_index()

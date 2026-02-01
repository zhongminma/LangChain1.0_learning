import json
import shutil
import sys
from pathlib import Path

# -----------------------------
# Make local imports always work
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import (  # noqa: E402
    DATA_FILE,
    STORAGE_DIR,
    CHROMA_DIR,
    CHUNKS_FILE,
    COLLECTION,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBED_MODEL,
)

from langchain_core.documents import Document  # noqa: E402
from langchain_text_splitters import RecursiveCharacterTextSplitter  # noqa: E402
from langchain_huggingface import HuggingFaceEmbeddings  # noqa: E402
from langchain_chroma import Chroma  # noqa: E402


def main(reset: bool = True) -> None:
    # 1) Validate paths
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"DATA_FILE not found: {DATA_FILE}\n"
            f"Expected aspirin.txt under: {DATA_FILE.parent}"
        )

    # 2) Prepare storage
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    if reset and CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR, ignore_errors=True)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    # 3) Load text
    text = DATA_FILE.read_text(encoding="utf-8")

    # 4) Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_text(text)

    docs = [
        Document(
            page_content=c,
            metadata={"source": DATA_FILE.name, "chunk_id": i},
        )
        for i, c in enumerate(chunks)
    ]

    # 5) Persist chunks.jsonl (for BM25/debug/regression)
    with CHUNKS_FILE.open("w", encoding="utf-8") as f:
        for d in docs:
            f.write(
                json.dumps(
                    {"text": d.page_content, "metadata": d.metadata},
                    ensure_ascii=False,
                )
                + "\n"
            )

    # 6) Build vector store
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION,
    )

    print(f"✅ Ingested {len(docs)} chunks")
    print(f"   - DATA_FILE : {DATA_FILE}")
    print(f"   - CHUNKS    : {CHUNKS_FILE}")
    print(f"   - CHROMA_DB : {CHROMA_DIR}")
    print(f"   - COLLECTION: {COLLECTION}")
    print(f"   - chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}, embed={EMBED_MODEL}")


if __name__ == "__main__":
    main(reset=True)

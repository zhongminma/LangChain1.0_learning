from pathlib import Path
from typing import List
from langchain_core.documents import Document

def load_raw_texts(raw_dir: Path) -> List[Document]:
    """
    Minimal loader: read .txt/.md as plain text.
    (You can extend to PDF/HTML later.)
    """
    docs: List[Document] = []
    for p in raw_dir.rglob("*"):
        if p.suffix.lower() not in {".txt", ".md"}:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        docs.append(Document(page_content=text, metadata={"source": str(p)}))
    return docs

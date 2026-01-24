from dataclasses import dataclass
from pathlib import Path
import os

@dataclass(frozen=True)
class RAGConfig:
    # Paths
    project_root: Path = Path(__file__).resolve().parents[2]  # rag-demo/
    raw_dir: Path = project_root / "data" / "raw"
    chroma_dir: Path = project_root / "data" / "chroma"

    # Models
    chat_model: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    embed_model: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

    # Chunking
    chunk_size: int = 800
    chunk_overlap: int = 120

    # Retrieval
    k: int = 4

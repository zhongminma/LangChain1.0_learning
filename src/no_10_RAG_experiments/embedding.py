from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

text = (Path(__file__).parent / "data" / "aspirin.txt").read_text(encoding="utf-8")
chunks = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=80).split_text(text)
emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
Chroma.from_texts(chunks, emb, persist_directory=str(Path(__file__).parent / "chroma_db"), collection_name="rag_demo")
print(f"✅ indexed {len(chunks)} chunks into chroma_db/")

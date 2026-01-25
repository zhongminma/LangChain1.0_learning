from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1️⃣ 读取原始文本
DATA_FILE = Path(__file__).parent / "data" / "aspirin.txt"
text = DATA_FILE.read_text(encoding="utf-8")

print("=" * 80)
print("ORIGINAL TEXT (preview)")
print(text[:300])
print("=" * 80)


def run_chunking(chunk_size: int, chunk_overlap: int):
    print(f"\n\n🧩 chunk_size={chunk_size}, overlap={chunk_overlap}")
    print("-" * 80)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_text(text)

    print(f"Total chunks: {len(chunks)}\n")

    for i, c in enumerate(chunks):
        print(f"--- Chunk {i} | len={len(c)} ---")
        print(c)
        print("-" * 80)


# 2️⃣ Case A：小 chunk + 小 overlap（看得最清楚）
run_chunking(chunk_size=200, chunk_overlap=40)

# 3️⃣ Case B：中等 chunk + 中等 overlap（最常见 RAG 配置）
run_chunking(chunk_size=400, chunk_overlap=80)

# 4️⃣ Case C：大 chunk + 小 overlap（适合长上下文模型）
run_chunking(chunk_size=800, chunk_overlap=100)

from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from typing import Any, Dict, List
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

# tool decorator：优先用 langchain_core，万一没有再降级
try:
    from langchain_core.tools import tool
except Exception:
    from langchain.tools import tool  # 老版本 fallback

from retriever import retrieve, format_context, retrieve_with_debug

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "storage" / "retrieval_logs.jsonl"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

@tool
def rag_hybrid_search(query: str) -> str:
    """Hybrid search (BM25 + dense) with cross-encoder reranking. Returns grounded context snippets."""
    docs, debug = retrieve_with_debug(query)
    rec = debug.get("recall", {})
    rer = debug.get("rerank", {})
    # ---- Console log (可观测) ----
    print("\n[TOOL CALL] rag_hybrid_search")
    print("  query:", query)
    print("  bm25(top ids):", rec.get("bm25_top_chunk_ids"))
    print("  dense(top ids):", rec.get("dense_top_chunk_ids"))
    print("  fusion(top ids):", rec.get("fusion_top_chunk_ids"))
    print("  rerank(top ids):", rer.get("rerank_top_chunk_ids"))
    print("  rerank(scores):", [round(x, 4) for x in (rer.get("rerank_scores") or [])], "\n")

    # ---- Persist log (回归测试) ----
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(debug, ensure_ascii=False) + "\n")

    if not docs:
        return "No relevant context found."
    return format_context(docs)


def _extract_tool_calls(ai_msg) -> List[Dict[str, Any]]:
    """
    兼容不同版本：tool_calls 可能在 ai_msg.tool_calls 或 ai_msg.additional_kwargs['tool_calls']
    返回格式统一为: [{"id": "...", "name": "...", "args": {...}}, ...]
    """
    if hasattr(ai_msg, "tool_calls") and ai_msg.tool_calls:
        return ai_msg.tool_calls

    ak = getattr(ai_msg, "additional_kwargs", None) or {}
    tc = ak.get("tool_calls")
    if not tc:
        return []

    # OpenAI 原始格式适配
    out = []
    for call in tc:
        fn = call.get("function", {}) or {}
        name = fn.get("name")
        args = fn.get("arguments")
        # arguments 可能是 JSON 字符串
        if isinstance(args, str):
            import json
            try:
                args = json.loads(args)
            except Exception:
                args = {"query": args}
        out.append({"id": call.get("id", ""), "name": name, "args": args or {}})
    return out


def run_agent(question: str, max_steps: int = 6) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 关键：bind_tools 让模型“知道”你有哪些工具可用
    llm_tools = llm.bind_tools([rag_hybrid_search])

    messages = [
        SystemMessage(content=(
            "You are a medical safety assistant. "
            "For ANY question about medicines, side effects, contraindications, bleeding risk, or children, "
            "you MUST call rag_hybrid_search first before answering. "
            "Then answer using ONLY the retrieved context. "
            "Cite the context as [1], [2], etc. "
            "If the context does not contain the answer, say: 'I don't know based on the provided documents.'"
        )),
        HumanMessage(content=question),
    ]

    for _ in range(max_steps):
        ai = llm_tools.invoke(messages)

        tool_calls = _extract_tool_calls(ai)
        if not tool_calls:
            # 没有工具调用 => 直接是最终回答
            final = ai.content if isinstance(ai.content, str) else str(ai.content)

            # Guard: If it answered without citations, force one more retrieval cycle
            if ("[" not in final) and ("No relevant" not in final):
                messages.append(HumanMessage(
                    content="You must cite sources as [1], [2] based only on retrieved context. Try again."))
                continue

            return final
            return ai.content if isinstance(ai.content, str) else str(ai.content)

        # 有工具调用：逐个执行，然后把 ToolMessage 追加回 messages
        messages.append(ai)

        for call in tool_calls:
            if call["name"] != "rag_hybrid_search":
                # 理论上不会发生，但防御一下
                messages.append(ToolMessage(tool_call_id=call.get("id", ""), content="Unknown tool"))
                continue

            query = call.get("args", {}).get("query", "")
            result = rag_hybrid_search.invoke({"query": query})  # 注意：tool 需要用 .invoke
            messages.append(ToolMessage(tool_call_id=call.get("id", ""), content=str(result)))

    return "Reached max_steps without a final answer."


def main():
    while True:
        q = input("\nYou> ").strip()
        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            break
        ans = run_agent(q)
        print("\nAssistant>\n", ans)


if __name__ == "__main__":
    main()

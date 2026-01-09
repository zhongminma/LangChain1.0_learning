import { TopicSummary } from "@/types/llm";

function getOrCreateId(key: string) {
  if (typeof window === "undefined") return "";
  const existing = localStorage.getItem(key);
  if (existing) return existing;
  const id = crypto.randomUUID();
  localStorage.setItem(key, id);
  return id;
}

export async function invokeLLM(topic: string): Promise<TopicSummary> {
  // 你后续可以替换成真实登录态的 user_id
  const user_id = getOrCreateId("demo_user_id");
  // 每个“会话/页面”一个 conversation_id（也可以按聊天窗口生成）
  const conversation_id = getOrCreateId("demo_conversation_id");

  // 每次请求一个 request_id，方便排查
  const request_id = crypto.randomUUID();

  const res = await fetch("http://localhost:8000/api/llm/invoke", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-request-id": request_id
    },
    body: JSON.stringify({
      input: { topic },
      config: {
        tags: ["frontend", "topic_chain"],
        metadata: { user_id, conversation_id, request_id },
      },
    }),
  });

  if (!res.ok) {
    // 让你一眼看到 request_id，去 LangSmith 搜它就能定位 trace
    const text = await res.text();
    throw new Error(`LLM request failed (request_id=${request_id}): ${text}`);
  }

  const json = await res.json();
  return json.output;
}

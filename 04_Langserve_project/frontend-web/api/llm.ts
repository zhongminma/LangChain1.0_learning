import { TopicSummary } from "@/types/llm";

export async function invokeLLM(topic: string): Promise<TopicSummary> {
  const res = await fetch("http://localhost:8000/api/llm/invoke", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      input: { topic }
    })
  });

  const json = await res.json();
  return json.output;
}

"use client";

import { useState } from "react";
import { invokeLLM } from "@/api/llm";
import { LLMResult } from "@/components/LLMResult";
import { TopicSummary } from "@/types/llm";

export default function HomePage() {
  const [topic, setTopic] = useState("");
  const [data, setData] = useState<TopicSummary | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setLoading(true);
    try {
      const result = await invokeLLM(topic);
      setData(result);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <input
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter a topic"
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Loading..." : "Ask LLM"}
      </button>

      {data && <LLMResult data={data} />}
    </main>
  );
}

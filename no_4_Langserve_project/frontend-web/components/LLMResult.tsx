import { TopicSummary } from "@/types/llm";

export function LLMResult({ data }: { data: TopicSummary }) {
  return (
    <div>
      <h2>{data.title}</h2>
      <p>{data.summary}</p>

      <h3>Pros</h3>
      <ul>
        {data.pros.map((p, i) => <li key={i}>{p}</li>)}
      </ul>

      <h3>Cons</h3>
      <ul>
        {data.cons.map((c, i) => <li key={i}>{c}</li>)}
      </ul>
    </div>
  );
}

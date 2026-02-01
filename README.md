# LLM Framework Playground: From Foundations to AI Agents
**LangChain v1.x · LangGraph · LangServe · RAG · Agentic RAG**

This repository is a hands-on **LLM engineering playground** focused on building, orchestrating, and operating **production-oriented LangChain workflows**.
It covers both **deterministic RAG pipelines** and **agentic RAG systems**, where retrieval is exposed as a tool and autonomously invoked by an AI agent.
It explores how large language models can be integrated into real backend systems with attention to **state management, reliability, observability, and scalability**.
Rather than isolated demos, this project emphasizes **engineering patterns and trade-offs** encountered when applying LLMs in real-world applications.

LangChain Framework v1.0 was released on October 22, 2025, and it is a vast improvement over the 0.3 version of the LangChain framework.

---

## Project Goals

- Explore **LangChain v1.x core abstractions** (Runnable, Prompt, Memory, Tools)
- Design **multi-turn, stateful chat workflows** with session-aware and user-aware memory
- Integrate LLM backends into real services using **LangServe + Next.js**
- Experiment with **streaming, async execution, and token usage tracking**
- Address production concerns such as:
  - Reliability and error handling
  - Rate limiting and middleware design
  - Observability and debugging (LangSmith)
  - State management with Redis and in-memory stores

---

## Technical Scope

- **LLM Orchestration**: LangChain v1.x (Runnable, PromptTemplate, Structured Output)
- **Stateful Workflows**: LangGraph
- **Backend Services**: LangServe (API exposure)
- **Frontend Integration**: Next.js
- **Memory & State**: In-memory history, Redis-backed chat history
- **Execution Models**: sync / async, stream / astream
- **Observability**: token usage tracking, LangSmith integration
- **Production Concerns**: error handling, rate limiting, logging

---

## Project Structure

### 1. Basic LangChain Building Blocks  
`src/no_01_basic_examples`

- LLM + Prompt + Chain composition
- Structured output examples:
  - String output
  - Pydantic models
  - Typed / structured responses
- XML output handling with normalization logic  
  (AOP-like preprocessing for consistent downstream parsing)

---

### 2. Prompt Engineering  
`src/no_02_prompt_template`

- String-based prompt templates
- ChatPromptTemplate usage
- Few-shot prompting
- Dynamic example selection using **Example Selector**

---

### 3. Runnable & Streaming  
`src/no_03_runnable_examples`

- Runnable execution patterns
- `stream` and `astream`
- Event-based streaming
- Token usage tracking using `BaseCallbackHandler`

---

### 4. LangServe Full-Stack Project  
`src/no_04_langserve_project`

- LLM backend exposed via **LangServe**
- **Next.js frontend** integration (see project-specific README for setup)
- Chat history strategies:
  - `session_id` + in-memory store
  - `session_id` + Redis
  - `user_id` + `conversation_id`
- Redis-backed `RunnableWithMessageHistory`
- LangSmith configuration for tracing and observability  
  https://smith.langchain.com/

---

### 5. Tools  
`src/no_05_tool_samples`

- `@tool` decorator usage
- `StructuredTool` examples
- Async and coroutine-based tool execution
- Error handling and tool invocation patterns

---

### 6. Agents  
`src/no_06_agent_examples`

- Agent invocation basics
- Debugging agent execution
- Streaming agents with tools
- Agents coordinating multiple tools

---

### 7. Middleware & Utilities  
`src/no_07_middleware_and_utils`

- Chat memory abstractions
- Redis or database-backed storage
- Token usage tracking
- Rate limiting
- Centralized logging utilities

---

### 8. Handlers  
`src/no_08_handlers`

- Centralized error handling strategies
- Consistent error response patterns for LLM services

---

### 9. LangGraph  
`src/no_09_langgraph`

- Stateful graph-based workflows
- Control-flow and state transition examples
- Counter-based LangGraph sample
- Chatbots MessagesState 
- mental mode 1/5: state-machin-agent (production mainly) 
- mental mode 2/5： MCP Agent (primary)
- mental mode 3/5：ReAct agent mode (seldom)
- mental mode 4/5：Supervisor agent mode (seldom)
- mental mode 4/5： Supervisor agent (PNG or mermaid) (seldom)
- mental mode 5/5： plan-and-execute (seldom)
  
---
### 10. RAG experiments  
`src/no_10_RAG_experiments`

- indexing
- chunking
- embedding
- hybrid_search

---

### 11. RAG project: RAG with LangChain 
`src/no_11_RAG_project`
### Architecture
```text
User Question
     ↓
Query Embedding
     ↓
Vector Store (Chroma)
     ↓
Top-K Relevant Chunks
     ↓
Context Assembly
     ↓
LLM Answer (Grounded)
```
### Workflow
- Ingestion (Offline)
```text
Raw documents
 → Chunking
 → Embeddings
 → Chroma vector store (persistent)
```
- Query & Generation (Online)
```text
User question
 → Vector similarity search
 → Top-K chunks
 → Prompt with context
 → LLM answer
```
- run 
```text
python src/ingest.py

python src/chat.py
```
---

### 12. AI Agent: Agentic RAG (RAG-as-Tool)
`src/no_12_AI_agent_project`

This module demonstrates an **agentic RAG architecture**, where retrieval is not a fixed pipeline step
but is instead exposed as a callable tool and invoked autonomously by the LLM.

### Architecture

```text
User Question
     ↓
LLM (Agent)
     ↓ decides whether to retrieve
RAG Tool (Hybrid Retrieval + Rerank)
     ↓
Grounded Context
     ↓
LLM Final Answer (with citations)
```
Key features:
- RAG implemented as a tool (RAG-as-Tool)
- Hybrid retrieval (BM25 + dense vector search)
- Cross-encoder reranking for improved top-k relevance
- Citation-enforced, grounded generation
- Retrieval observability and regression logging (`storage/retrieval_logs.jsonl`)

---
## Environment Setup

- Python 3.x
- pip / virtual environment
- LangChain v1.x
- OpenAI and/or Gemini API keys

High-level setup steps:

1. Create and activate a virtual environment
2. Install required pip packages
3. Configure OpenAI / Gemini credentials via environment variables
4. (Optional) Configure Redis and LangSmith for extended functionality

---

## Why This Project Matters

This project reflects **real-world challenges in LLM-powered systems**, including:

- Managing conversational state across sessions and users
- Balancing flexibility and reliability in prompt and chain design
- Observing and debugging complex LLM workflows
- Integrating LLMs into existing backend and frontend architectures

It is intentionally designed to mirror **production-oriented thinking**
rather than tutorial-style examples.

---

## Notes

- This repository focuses on **engineering patterns**, not model benchmarking
- Examples are intentionally modular to support experimentation and extension
- The project evolves alongside LangChain and LLM ecosystem changes

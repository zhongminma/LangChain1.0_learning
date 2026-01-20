# LLM Engineering Playground  - Python based
**LangChain v1.x · LangGraph · LangServe · RAG Experiments**

This repository is a hands-on **LLM engineering playground** focused on building, orchestrating, and operating **production-oriented LangChain workflows**.
It explores how large language models can be integrated into real backend systems with attention to **state management, reliability, observability, and scalability**.
Rather than isolated demos, this project emphasizes **engineering patterns and trade-offs** encountered when applying LLMs in real-world applications.

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

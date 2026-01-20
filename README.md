# LLM Engineering Playground (LangChain v1.x, LangGraph, LangServe, RAG)
This repository is a hands-on LLM engineering playground focused on building, orchestrating, and operating production-oriented LangChain workflows, including memory management, tool integration, streaming, and reliability concerns.

## Project Goals
- Explore LangChain v1.x core abstractions (Runnable, Prompt, Memory, Tools)
- Design multi-turn chat workflows with session-aware and user-aware memory
- Integrate LLM backends with real services (LangServe + Next.js)
- Address production concerns such as observability, token usage, rate limiting, error handling, and state management

## Technical Scope
- LangChain v1.x (Runnable, PromptTemplate, Structured Output)
- LangGraph for stateful LLM workflows
- LangServe for backend API exposure
- Redis / In-memory chat history
- Streaming, async execution, and token tracking
- Error handling, middleware, and rate limiting
- Next.js frontend integration

## Project Structure

### 1. Basic LangChain Building Blocks - src/no_01_basic_examples
- LLM + Prompt + Chain composition
- Structured output (Pydantic, JSON)
- XML output handling with normalization (AOP-like preprocessing)

### 2. Prompt Engineering - src/no_02_prompt_template
- String and chat prompt templates
- Few-shot prompting
- Example selectors for dynamic prompt composition

### 3. Runnable & Streaming - src/no_03_runnable_examples
- stream / astream execution
- Event streaming
- Token usage tracking via BaseCallBackHandler

### 4. LangServe Full-Stack Project - no_04_langserve_project
- LLM backend exposed via LangServe
- Next.js frontend integration
- Chat history with:
  - session_id (in-memory / Redis)
  - user_id + conversation_id
- Redis-backed RunnableWithMessageHistory
- LangSmith configuration for observability

### 5. Tools - src/no_05_tool_samples
- @tool decorator usage
- StructuredTool with async/coroutine support

### 6. Agents - src/no_06_agent_examples
- Agent invocation and debugging
- Streaming agents with single and multiple tools

### 7. Middleware & Utilities -  src/no_07__middleware_and_utils
- Memory abstraction (InMemoryChatMessageHistory)
- Redis / database support
- Token usage tracking
- Rate limiting
- Logging utilities

### 8. Handlers - src/no_08_handlers
- Centralized error handling

### 9. LangGraph - src/no_9_LangGraph
- Stateful graph-based workflows
- Counter and control-flow examples
